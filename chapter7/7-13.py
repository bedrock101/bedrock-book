import boto3
import os

def lambda_handler(event, context):
    region = os.environ['AWS_REGION']
    bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name=region)
    
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    
    conversation = [
      {
        "role": "user",
        "content": [{"text": "Bedrock은 너무 방대한 서비스입니다."}],
      }
    ]
    
    response = bedrock_runtime.converse(
    modelId=model_id,
    messages=conversation,
    inferenceConfig={"maxTokens": 512, "temperature": 1, "topP": 0.9},
    )
    
    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)
