// background.js — Service Worker for the Cookie Grabber extension
//
// Handles the "grabAndSend" message from popup.html:
//   1. Gets all cookies for the specified domain
//   2. Encrypts them with AES-256-GCM (key derived via PBKDF2 from master password)
//   3. Sends the encrypted blob to the local WebSocket server
//
// Security: cookies are encrypted BEFORE leaving the browser.
// The server stores only the encrypted blob — it never sees plaintext values.

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.action === "grabAndSend") {
    handleGrabAndSend(message)
      .then(result => sendResponse(result))
      .catch(err => sendResponse({ ok: false, error: err.message }));
    return true; // keep message channel open for the async response
  }
});

async function handleGrabAndSend({ domain, serverUrl, masterPassword }) {
  // 1. Collect all cookies for the domain
  const cookies = await chrome.cookies.getAll({ domain });
  if (cookies.length === 0) {
    return { ok: false, error: `No cookies found for domain: ${domain}` };
  }

  // 2. Serialize only the fields the CLI needs
  const cookieData = cookies.map(c => ({
    name: c.name,
    value: c.value,
    domain: c.domain,
    path: c.path,
    secure: c.secure,
    httpOnly: c.httpOnly,
  }));
  const plaintext = new TextEncoder().encode(JSON.stringify(cookieData));

  // 3. Derive AES-256 key from master password using PBKDF2
  const salt = crypto.getRandomValues(new Uint8Array(32));
  const iv   = crypto.getRandomValues(new Uint8Array(12));

  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(masterPassword),
    { name: "PBKDF2" },
    false,
    ["deriveKey"]
  );
  const key = await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: 600_000, hash: "SHA-256" },
    keyMaterial,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt"]
  );

  // 4. Encrypt with AES-256-GCM
  const ciphertext = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    plaintext
  );

  // 5. Base64-encode for JSON transport
  const toBase64 = buf => btoa(String.fromCharCode(...new Uint8Array(buf)));
  const payload = {
    domain,
    encrypted: toBase64(ciphertext),
    salt:      toBase64(salt),
    iv:        toBase64(iv),
  };

  // 6. Send to local server via WebSocket
  const result = await sendToServer(serverUrl, payload);
  return { ...result, count: cookies.length };
}

function sendToServer(serverUrl, payload) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(serverUrl);
    let settled = false;

    const settle = result => {
      if (!settled) {
        settled = true;
        try { ws.close(); } catch (_) {}
        if (result.ok) resolve(result);
        else reject(new Error(result.error || "Unknown server error"));
      }
    };

    ws.addEventListener("open",    ()  => ws.send(JSON.stringify(payload)));
    ws.addEventListener("message", e   => settle(JSON.parse(e.data)));
    ws.addEventListener("error",   ()  => settle({ ok: false, error: "WebSocket connection failed — is the server running?" }));
    ws.addEventListener("close",   ()  => { if (!settled) settle({ ok: false, error: "Connection closed unexpectedly" }); });

    // Safety timeout
    setTimeout(() => settle({ ok: false, error: "Timeout — server did not respond in 10s" }), 10_000);
  });
}
