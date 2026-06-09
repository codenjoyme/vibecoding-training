#!/usr/bin/env node
/**
 * codemie-relay.js
 * Thin HTTP relay: accepts any Bearer key on port 4002,
 * forwards to codemie proxy on port 4001 with the correct gateway key.
 *
 * Patches applied:
 *  1. Authorization header → Bearer codemie-proxy (any incoming key accepted)
 *  2. temperature + top_p → remove top_p (litellm/Bedrock Claude rejects both)
 *  3. model fake-id in request → real CodeMie model id (via MODEL_MAP)
 *  4. model in responses (streaming + non-streaming) → echoed back as the fake-id
 *     (Copilot needs a recognized model name in responses to resolve tokenizer)
 *
 * Multi-model support via chatLanguageModels.json:
 *  Add "realModelId" to any model entry in chatLanguageModels.json:
 *    { "id": "gpt-4", "realModelId": "claude-sonnet-4-6", "name": "...", ... }
 *  The relay reads the config at startup and builds MODEL_MAP automatically.
 *  No need to edit this file when adding new models — only edit chatLanguageModels.json.
 *
 * Config file locations (searched in order):
 *  Windows: %APPDATA%\Code - Insiders\User\chatLanguageModels.json
 *           %APPDATA%\Code\User\chatLanguageModels.json
 *  macOS:   ~/Library/Application Support/Code - Insiders/User/chatLanguageModels.json
 *           ~/Library/Application Support/Code/User/chatLanguageModels.json
 *  Linux:   ~/.config/Code - Insiders/User/chatLanguageModels.json
 *           ~/.config/Code/User/chatLanguageModels.json
 *
 * Start: node codemie-relay.js
 */
'use strict';
const http = require('http');
const fs   = require('fs');
const path = require('path');
const os   = require('os');

const TARGET_HOST = '127.0.0.1';
const TARGET_PORT = 4001;
const GATEWAY_KEY = 'codemie-proxy';
const RELAY_PORT  = 4002;

// ── Locate chatLanguageModels.json ──────────────────────────────────────────
function findConfigPaths() {
  const home = os.homedir();
  const platform = process.platform;
  let base;
  if (platform === 'win32') {
    base = process.env.APPDATA || path.join(home, 'AppData', 'Roaming');
    return [
      path.join(base, 'Code - Insiders', 'User', 'chatLanguageModels.json'),
      path.join(base, 'Code',            'User', 'chatLanguageModels.json'),
    ];
  } else if (platform === 'darwin') {
    base = path.join(home, 'Library', 'Application Support');
    return [
      path.join(base, 'Code - Insiders', 'User', 'chatLanguageModels.json'),
      path.join(base, 'Code',            'User', 'chatLanguageModels.json'),
    ];
  } else {
    base = process.env.XDG_CONFIG_HOME || path.join(home, '.config');
    return [
      path.join(base, 'Code - Insiders', 'User', 'chatLanguageModels.json'),
      path.join(base, 'Code',            'User', 'chatLanguageModels.json'),
    ];
  }
}

// ── Build MODEL_MAP from config ─────────────────────────────────────────────
// Reads all entries that have "realModelId" set.
// Falls back to hardcoded defaults if config is missing or has no realModelId entries.
const FALLBACK_MAP = {
  'gpt-4':   'claude-sonnet-4-6',
  'gpt-4o':  'claude-opus-4-5',
};

function buildModelMap() {
  const candidates = findConfigPaths();
  for (const p of candidates) {
    if (!fs.existsSync(p)) continue;
    try {
      const raw = fs.readFileSync(p, 'utf8');
      const entries = JSON.parse(raw);
      const map = {};
      for (const vendor of entries) {
        for (const model of (vendor.models || [])) {
          if (model.id && model.realModelId) {
            map[model.id] = model.realModelId;
          }
        }
      }
      if (Object.keys(map).length > 0) {
        console.log('model map loaded from: ' + p);
        return map;
      }
      console.log('config found at ' + p + ' but no realModelId entries — using fallback');
      return FALLBACK_MAP;
    } catch (e) {
      console.log('warning: could not parse ' + p + ': ' + e.message);
    }
  }
  console.log('chatLanguageModels.json not found — using fallback MODEL_MAP');
  return FALLBACK_MAP;
}

const MODEL_MAP = buildModelMap();

function toRealModel(fakeId) {
  return MODEL_MAP[fakeId] || fakeId;
}

function toFakeModel(realId, originalFakeId) {
  return originalFakeId || realId;
}

// ── HTTP relay ───────────────────────────────────────────────────────────────
const server = http.createServer((req, res) => {
  const chunks = [];
  req.on('data', (chunk) => chunks.push(chunk));
  req.on('end', () => {
    let body = Buffer.concat(chunks);
    let fakeModelId = null;

    if (req.method !== 'GET' && body.length > 0) {
      try {
        const parsed = JSON.parse(body.toString('utf8'));

        // Patch 1: remove top_p when temperature is also present
        if (parsed.temperature !== undefined && parsed.top_p !== undefined) {
          delete parsed.top_p;
        }

        // Patch 2: rewrite model name from fake id to real model
        if (parsed.model) {
          fakeModelId = parsed.model;
          parsed.model = toRealModel(parsed.model);
        }

        body = Buffer.from(JSON.stringify(parsed), 'utf8');
      } catch (e) { /* not JSON, forward as-is */ }
    }

    const headers = Object.assign({}, req.headers, {
      host:             TARGET_HOST + ':' + TARGET_PORT,
      authorization:    'Bearer ' + GATEWAY_KEY,
      'content-length': body.length,
    });

    const options = {
      hostname: TARGET_HOST,
      port:     TARGET_PORT,
      path:     req.url,
      method:   req.method,
      headers:  headers,
    };

    const proxyReq = http.request(options, (proxyRes) => {
      const isStream = (proxyRes.headers['content-type'] || '').includes('text/event-stream');

      if (isStream) {
        res.writeHead(proxyRes.statusCode, proxyRes.headers);
        let lineBuffer = '';
        proxyRes.on('data', (chunk) => {
          lineBuffer += chunk.toString('utf8');
          const lines = lineBuffer.split('\n');
          lineBuffer = lines.pop();
          const out = lines.map(line => {
            if (!line.startsWith('data: ') || line.trimEnd() === 'data: [DONE]') return line;
            try {
              const parsed = JSON.parse(line.slice(6));
              parsed.model = toFakeModel(parsed.model, fakeModelId);
              return 'data: ' + JSON.stringify(parsed);
            } catch (e) { return line; }
          }).join('\n') + '\n';
          res.write(out);
        });
        proxyRes.on('end', () => {
          if (lineBuffer) {
            if (lineBuffer.startsWith('data: ') && lineBuffer.trimEnd() !== 'data: [DONE]') {
              try {
                const parsed = JSON.parse(lineBuffer.slice(6));
                parsed.model = toFakeModel(parsed.model, fakeModelId);
                res.write('data: ' + JSON.stringify(parsed) + '\n');
                res.end();
                return;
              } catch (e) {}
            }
            res.write(lineBuffer);
          }
          res.end();
        });
      } else {
        const respChunks = [];
        proxyRes.on('data', (c) => respChunks.push(c));
        proxyRes.on('end', () => {
          let respBody = Buffer.concat(respChunks).toString('utf8');
          try {
            const parsed = JSON.parse(respBody);
            if (parsed.model !== undefined) {
              parsed.model = toFakeModel(parsed.model, fakeModelId);
            }
            respBody = JSON.stringify(parsed);
          } catch (e) { /* not JSON, leave as-is */ }
          const outBuf = Buffer.from(respBody, 'utf8');
          const respHeaders = Object.assign({}, proxyRes.headers, {
            'content-length': outBuf.length,
          });
          res.writeHead(proxyRes.statusCode, respHeaders);
          res.end(outBuf);
        });
      }
    });

    proxyReq.on('error', (err) => {
      res.writeHead(502);
      res.end(JSON.stringify({ error: 'relay error: ' + err.message }));
    });

    proxyReq.write(body);
    proxyReq.end();
  });
});

server.listen(RELAY_PORT, '127.0.0.1', () => {
  console.log('codemie-relay listening on http://127.0.0.1:' + RELAY_PORT + '/v1');
  console.log('forwarding to http://127.0.0.1:' + TARGET_PORT + ' with key ' + GATEWAY_KEY);
  console.log('model map:');
  Object.entries(MODEL_MAP).forEach(([fake, real]) => {
    console.log('  ' + fake + ' → ' + real);
  });
});
