#!/usr/bin/env bash
# List available DIAL models/deployments
# Usage: DIAL_API_KEY="your-key" ./test-dial-models-list-linux.sh

BASE_URL="https://ai-proxy.lab.epam.com"
API_KEY="${DIAL_API_KEY:-YOUR_API_KEY_HERE}"

echo "Trying /openai/models..."
curl -s -H "api-key: $API_KEY" "$BASE_URL/openai/models" \
  | python3 -c "import sys,json; data=json.load(sys.stdin); [print(m['id']) for m in data.get('data',[])]" \
  2>/dev/null || echo "  (endpoint not available or parse error)"

echo ""
echo "Trying /openai/deployments..."
curl -s -H "api-key: $API_KEY" "$BASE_URL/openai/deployments" \
  | python3 -c "import sys,json; data=json.load(sys.stdin); [print(m['id']) for m in data.get('data',[])]" \
  2>/dev/null || echo "  (endpoint not available or parse error)"
