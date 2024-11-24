aws bedrock-runtime converse \
--model-id us.anthropic.claude-3-haiku-20240307-v1:0 --region us-west-2 \
--messages '[{"role": "user", "content": [{"text": "Hello"}]}]' \
--inference-config '{"maxTokens": 512, "temperature": 0.5, "topP": 0.9}'
