#!/usr/bin/env node
/**
 * codemie-relay.js
 * Thin HTTP relay: accepts any Bearer key on port 4002,
 * forwards to codemie proxy on port 4001 with the correct gateway key.
 * Start: node codemie-relay.js
 */
'use strict';
const http = require('http');

const TARGET_HOST = '127.0.0.1';
const TARGET_PORT = 4001;
const GATEWAY_KEY = 'codemie-proxy';
const RELAY_PORT = 4002;

const server = http.createServer((req, res) => {
  // Collect body so we can patch it before forwarding
  const chunks = [];
  req.on('data', (chunk) => chunks.push(chunk));
  req.on('end', () => {
    let body = Buffer.concat(chunks);

    // Patch: if both temperature and top_p are present, remove top_p.
    // litellm/Bedrock Claude rejects requests that have both.
    if (req.method !== 'GET' && body.length > 0) {
      try {
        const parsed = JSON.parse(body.toString('utf8'));
        if (parsed.temperature !== undefined && parsed.top_p !== undefined) {
          delete parsed.top_p;
          body = Buffer.from(JSON.stringify(parsed), 'utf8');
        }
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

    const proxy = http.request(options, (proxyRes) => {
      res.writeHead(proxyRes.statusCode, proxyRes.headers);
      proxyRes.pipe(res, { end: true });
    });

    proxy.on('error', (err) => {
      res.writeHead(502);
      res.end(JSON.stringify({ error: 'relay error: ' + err.message }));
    });

    proxy.write(body);
    proxy.end();
  });
});

server.listen(RELAY_PORT, '127.0.0.1', () => {
  console.log('codemie-relay listening on http://127.0.0.1:' + RELAY_PORT + '/v1');
  console.log('forwarding to http://127.0.0.1:' + TARGET_PORT + ' with key ' + GATEWAY_KEY);
});
