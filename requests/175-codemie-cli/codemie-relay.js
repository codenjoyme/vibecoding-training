#!/usr/bin/env node
/**
 * codemie-relay.js
 * Thin HTTP relay: accepts any Bearer key on port 4002,
 * forwards to codemie proxy on port 4001 with the correct gateway key.
 *
 * Patches applied:
 *  1. Authorization header → Bearer codemie-proxy (any incoming key accepted)
 *  2. temperature + top_p → remove top_p (litellm/Bedrock Claude rejects both)
 *  3. model "gpt-4" in request → "claude-sonnet-4-6" (Copilot sends id from config)
 *  4. model in responses (streaming + non-streaming) → "gpt-4"
 *     (Copilot needs a recognized model name in responses to resolve tokenizer)
 *
 * Start: node codemie-relay.js
 */
'use strict';
const http = require('http');

const TARGET_HOST = '127.0.0.1';
const TARGET_PORT = 4001;
const GATEWAY_KEY = 'codemie-proxy';
const RELAY_PORT = 4002;
const FAKE_MODEL = 'gpt-4';          // what Copilot sees (known tokenizer)
const REAL_MODEL = 'claude-sonnet-4-6'; // what codemie proxy receives

const server = http.createServer((req, res) => {
  const chunks = [];
  req.on('data', (chunk) => chunks.push(chunk));
  req.on('end', () => {
    let body = Buffer.concat(chunks);

    if (req.method !== 'GET' && body.length > 0) {
      try {
        const parsed = JSON.parse(body.toString('utf8'));

        // Patch 1: remove top_p when temperature is also present
        if (parsed.temperature !== undefined && parsed.top_p !== undefined) {
          delete parsed.top_p;
        }

        // Patch 2: rewrite model name from Copilot's fake id to real model
        if (parsed.model === FAKE_MODEL) {
          parsed.model = REAL_MODEL;
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
              parsed.model = FAKE_MODEL;
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
                parsed.model = FAKE_MODEL;
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
            if (parsed.model) parsed.model = FAKE_MODEL;
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
  console.log('model spoof: ' + FAKE_MODEL + ' → ' + REAL_MODEL + ' (request) / ' + REAL_MODEL + ' → ' + FAKE_MODEL + ' (response)');
});
