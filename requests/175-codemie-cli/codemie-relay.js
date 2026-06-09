#!/usr/bin/env node
/**
 * codemie-relay.js
 * Thin HTTP relay: accepts any Bearer key on port 4002,
 * forwards to codemie proxy on port 4001 with the correct gateway key.
 *
 * Patches applied:
 *  1. Authorization header -> Bearer codemie-proxy (any incoming key accepted)
 *  2. temperature + top_p -> remove top_p (litellm/Bedrock Claude rejects both)
 *  3. model id in request -> real CodeMie model id (via MODEL_MAP)
 *  4. model in responses (streaming + non-streaming) -> echoed back as original fake id
 *     (Copilot needs a recognized model name in responses to resolve tokenizer)
 *
 * MODEL_MAP is built at startup from chatLanguageModels.json.
 * Add "realModelId" to each model entry:
 *   { "id": "gpt-4",    "realModelId": "claude-sonnet-4-6", ... }
 *   { "id": "gpt-4o",   "realModelId": "claude-opus-4-6",   ... }
 * Relay reads all entries with realModelId and builds the map automatically.
 * If the file is not found or has no realModelId entries, hardcoded defaults are used.
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

// ---- Load FAKE_MODEL / REAL_MODEL from chatLanguageModels.json -------------
function findConfigPaths() {
  const home = os.homedir();
  if (process.platform === 'win32') {
    const base = process.env.APPDATA || path.join(home, 'AppData', 'Roaming');
    return [
      path.join(base, 'Code - Insiders', 'User', 'chatLanguageModels.json'),
      path.join(base, 'Code',            'User', 'chatLanguageModels.json'),
    ];
  } else if (process.platform === 'darwin') {
    const base = path.join(home, 'Library', 'Application Support');
    return [
      path.join(base, 'Code - Insiders', 'User', 'chatLanguageModels.json'),
      path.join(base, 'Code',            'User', 'chatLanguageModels.json'),
    ];
  } else {
    const base = process.env.XDG_CONFIG_HOME || path.join(home, '.config');
    return [
      path.join(base, 'Code - Insiders', 'User', 'chatLanguageModels.json'),
      path.join(base, 'Code',            'User', 'chatLanguageModels.json'),
    ];
  }
}

const FALLBACK_MAP = {
  'gpt-4':  'claude-sonnet-4-6',
  'gpt-4o': 'claude-opus-4-6-20260205',
};

function buildModelMap() {
  for (const p of findConfigPaths()) {
    if (!fs.existsSync(p)) continue;
    try {
      const entries = JSON.parse(fs.readFileSync(p, 'utf8'));
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
      console.log('config found at ' + p + ' but no realModelId entries -- using fallback');
    } catch (e) {
      console.log('warning: could not parse ' + p + ': ' + e.message);
    }
  }
  console.log('chatLanguageModels.json not found -- using fallback model map');
  return FALLBACK_MAP;
}

// MODEL_MAP: fake id (Copilot-known tokenizer name) -> real CodeMie model id
const MODEL_MAP = buildModelMap();

function toRealModel(fakeId) {
  return MODEL_MAP[fakeId] || fakeId;
}

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

        // Patch 2: rewrite model name from Copilot's fake id to real model
        if (parsed.model) {
          fakeModelId = parsed.model;
          parsed.model = toRealModel(parsed.model);
        }

        body = Buffer.from(JSON.stringify(parsed), 'utf8');
      } catch (e) { /* not JSON, forward as-is */ }
    }

    const headers = Object.assign({}, req.headers, {
      host: TARGET_HOST + ':' + TARGET_PORT,
      authorization: 'Bearer ' + GATEWAY_KEY,
      'content-length': body.length,
    });

    const options = {
      hostname: TARGET_HOST,
      port: TARGET_PORT,
      path: req.url,
      method: req.method,
      headers: headers,
    };

    const proxyReq = http.request(options, (proxyRes) => {
      const isStream = (proxyRes.headers['content-type'] || '').includes('text/event-stream');

      if (isStream) {
        // Streaming: forward headers as-is (Content-Length not applicable for SSE)
        res.writeHead(proxyRes.statusCode, proxyRes.headers);
        // Parse each SSE line and force-set model to FAKE_MODEL.
        // Regex approach misses "model":null — use per-line JSON parse instead.
        let lineBuffer = '';
        proxyRes.on('data', (chunk) => {
          lineBuffer += chunk.toString('utf8');
          const lines = lineBuffer.split('\n');
          lineBuffer = lines.pop(); // hold incomplete last line
          const out = lines.map(line => {
            if (!line.startsWith('data: ') || line.trimEnd() === 'data: [DONE]') return line;
            try {
              const parsed = JSON.parse(line.slice(6));
              if (fakeModelId) parsed.model = fakeModelId;
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
                if (fakeModelId) parsed.model = fakeModelId;
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
        // Non-streaming: buffer full body first, patch model, then send with correct Content-Length
        const respChunks = [];
        proxyRes.on('data', (c) => respChunks.push(c));
        proxyRes.on('end', () => {
          let respBody = Buffer.concat(respChunks).toString('utf8');
          try {
            const parsed = JSON.parse(respBody);
            if (parsed.model !== undefined && fakeModelId) parsed.model = fakeModelId;
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
    console.log('  ' + fake + ' -> ' + real);
  });
});
