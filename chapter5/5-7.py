messages = [{ "role": "user", "content": [{"text": input_text}] }]

response = bedrock_client.converse(
    modelId=model_id,
    messages=messages,
    toolConfig=tool_config
)

output_message = response['output']['message']
messages.append(output_message)
stop_reason = response['stopReason']
