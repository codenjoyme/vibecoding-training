[
	{
		"name": "CodeMie Proxy",
		"vendor": "customoai",
		"apiKey": "${input:chat.lm.secret.codemie}",
		"models": [
			{
				"id": "gpt-4",
				"name": "Claude Sonnet 4.6 (CodeMie)",
				"url": "http://127.0.0.1:4002/v1/chat/completions",
				"toolCalling": true,
				"vision": true,
				"maxInputTokens": 200000,
				"maxOutputTokens": 16000
			}
		]
	}
]