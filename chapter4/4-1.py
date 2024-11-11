from langchain_aws import ChatBedrockConverse

llm = ChatBedrockConverse(model="anthropic.claude-3-5-sonnet-20240620-v1:0")
response = llm.invoke("Titan Embedding V2는 몇 차원인가요?")

print(response.content)
