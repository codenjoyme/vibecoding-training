[
	{
		"name": "CodeMie Proxy",
		"vendor": "customoai",
		"apiKey": "${input:chat.lm.secret.codemie}",
		"models": [
			{
				"id": "gpt-4",
				"realModelId": "claude-sonnet-4-6",
				"name": "Claude Sonnet 4.6 (CodeMie)",
				"url": "http://127.0.0.1:4002/v1/chat/completions",
				"toolCalling": true,
				"vision": true,
				"maxInputTokens": 200000,
				"maxOutputTokens": 16000
			},
			{
				"id": "gpt-4o",
				"realModelId": "claude-opus-4-6",
				"name": "Claude Opus 4.6 (CodeMie)",
				"url": "http://127.0.0.1:4002/v1/chat/completions",
				"toolCalling": true,
				"vision": true,
				"maxInputTokens": 200000,
				"maxOutputTokens": 16000
			}
		]
	}
]