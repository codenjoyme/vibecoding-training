const grabBtn  = document.getElementById('grab');
const statusEl = document.getElementById('status');

function showStatus(msg, isOk) {
  statusEl.textContent = msg;
  statusEl.className   = isOk ? 'ok' : 'err';
  statusEl.style.display = 'block';
}

// Restore saved domain + server from extension storage
chrome.storage.local.get(['domain', 'serverUrl'], prefs => {
  if (prefs.domain)     document.getElementById('domain').value = prefs.domain;
  if (prefs.serverUrl)  document.getElementById('server').value = prefs.serverUrl;
});

grabBtn.addEventListener('click', async () => {
  const domain     = document.getElementById('domain').value.trim();
  const serverUrl  = document.getElementById('server').value.trim();
  const masterPass = document.getElementById('password').value;

  if (!domain || !masterPass) {
    showStatus('Please fill in domain and master password.', false);
    return;
  }

  // Save domain + server (not the password)
  chrome.storage.local.set({ domain, serverUrl });

  grabBtn.disabled = true;
  showStatus('Grabbing cookies…', true);

  try {
    const result = await chrome.runtime.sendMessage({
      action: 'grabAndSend',
      domain,
      serverUrl,
      masterPassword: masterPass,
    });

    if (result.ok) {
      showStatus(`✅ Sent ${result.count} cookies for ${result.domain}`, true);
      document.getElementById('password').value = ''; // clear password from DOM
    } else {
      showStatus(`❌ ${result.error}`, false);
    }
  } catch (err) {
    showStatus(`❌ ${err.message}`, false);
  } finally {
    grabBtn.disabled = false;
  }
});
