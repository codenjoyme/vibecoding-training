#!/bin/bash
# Bash script to test EPAM AI DIAL connection
# Replace YOUR_API_KEY_HERE with your actual API key from EPAM support

API_KEY="YOUR_API_KEY_HERE"
ENDPOINT="https://ai-proxy.lab.epam.com/openai/deployments/gpt-4o-mini-2024-07-18/chat/completions"

echo -e "\033[1;33mTesting EPAM AI DIAL connection...\033[0m"
echo -e "\033[1;36mEndpoint: $ENDPOINT\033[0m"
echo ""

echo -e "\033[1;33mSending request to DIAL...\033[0m"

response=$(curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "api-key: $API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Tell me about artificial intelligence in the style of a pirate."
      }
    ],
    "max_tokens": 500,
    "temperature": 0.7
  }')

if [ $? -eq 0 ]; then
    echo -e "\n\033[1;32mSuccess! Response received:\033[0m"
    echo -e "\033[1;32m================================\033[0m"
    
    # Extract and display the message content
    content=$(echo "$response" | grep -o '"content":"[^"]*"' | sed 's/"content":"//' | sed 's/"$//' | sed 's/\\n/\n/g')
    echo "$content"
    
    echo -e "\033[1;32m================================\033[0m"
    
    # Extract model and token info if available
    model=$(echo "$response" | grep -o '"model":"[^"]*"' | sed 's/"model":"//' | sed 's/"$//')
    if [ ! -z "$model" ]; then
        echo -e "\n\033[1;36mModel used: $model\033[0m"
    fi
    
else
    echo -e "\n\033[1;31mError occurred!\033[0m"
    echo -e "\n\033[1;33mTroubleshooting tips:\033[0m"
    echo "1. Verify your API key is correct"
    echo "2. Ensure you're connected to EPAM VPN"
    echo "3. Check that the model deployment name is current"
fi
