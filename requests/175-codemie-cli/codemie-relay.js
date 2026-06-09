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
 * Multi-model support:
 *  Add entries to MODEL_MAP below. The key is the "id" field in chatLanguageModels.json
 *  (must be a name Copilot knows, e.g. "gpt-4", "gpt-4o", "gpt-4o-mini").
 *  The value is the real model id sent to the CodeMie proxy.
 *
 * Start: node codemie-relay.js
 */
'use strict';
const http = require('http');

const TARGET_HOST = '127.0.0.1';
const TARGET_PORT = 4001;
const GATEWAY_KEY = 'codemie-proxy';
const RELAY_PORT = 4002;

// --- Multi-model map ---
// key   = fake model id used in chatLanguageModels.json (must be a Copilot-known tokenizer name)
// value = real model id forwarded to the CodeMie proxy
const MODEL_MAP = {
  'gpt-4':    'claude-sonnet-4-6',
  'gpt-4o':   'claude-opus-4-5',
  // Add more entries here as needed, e.g.:
  // 'gpt-4o-mini': 'gemini-2.5-flash',
};

// Fallback: if the incoming model id is not in MODEL_MAP, forward it unchanged.
function toRealModel(fakeId) {
  return MODEL_MAP[fakeId] || fakeId;
}

// Reverse: given a real model id, find the fake id to echo back.
// If not found, return the real id as-is (safe fallback).
function toFakeModel(realId, originalFakeId) {
  // Prefer the original fake id that was sent in the request (stored per-request).
  return originalFakeId || realId;
}

const server = http.createServer((req, res) => {
  const chunks = [];
  req.on('data', (chunk) => chunks.push(chunk));
  req.on('end', () => {
    let body = Buffer.concat(chunks);
    let fakeModelId = null; // remember what Copilot sent so we can echo it back

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
