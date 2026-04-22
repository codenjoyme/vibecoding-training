```
> npm install -g --install-links git+https://github.com/codenjoyme/apm-lite.git
 
npm error code 127
npm error git dep preparation failed
npm error command /Users/USER/.nvm/versions/node/v24.13.1/bin/node /Users/USER/.nvm/versions/node/v24.13.1/lib/node_modules/npm/bin/npm-cli.js install --force --cache=/Users/USER/.npm --prefer-offline=false --prefer-online=false --offline=false --no-progress --no-save --no-audit --include=dev --include=peer --include=optional --no-package-lock-only --no-dry-run
npm error npm warn using --force Recommended protections disabled.
npm error npm error code 127
npm error npm error path /Users/USER/.npm/_cacache/tmp/git-cloneJi1UPS
npm error npm error command failed
npm error npm error command sh -c tsc
npm error npm error sh: tsc: command not found
npm error npm error A complete log of this run can be found in: /Users/USER/.npm/_logs/2026-04-21T12_59_46_661Z-debug-0.log
npm error A complete log of this run can be found in: /Users/USER/.npm/_logs/2026-04-21T12_59_40_470Z-debug-0.log
```
агент смогу установаить но через пень колоду
```
cd /tmp && rm -rf apm-lite && git clone https://github.com/codenjoyme/apm-lite.git && cd apm-lite && npm install && npm install -g .
```