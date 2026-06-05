[
    {
		"name": "OpenAI Compatible",
		"vendor": "customoai",
		"apiKey": "${input:chat.lm.secret.dial}",
		"models": [
			{
				"id": "gpt-4o-2024-11-20",
				"name": "Claude Sonnet 4.6 (DIAL)",
				"url": "http://localhost:4000/openai/deployments/claude-sonnet-4-6@default/chat/completions",
				"toolCalling": true,
				"vision": true,
				"maxInputTokens": 80000,
				"maxOutputTokens": 16000
			}
		]
	}
]