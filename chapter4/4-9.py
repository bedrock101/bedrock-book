import boto3

bedrock_agent_runtime = boto3.client(service_name = "bedrock-agent-runtime")

def retrieve(query, kbId):
    modelArn = 'arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
    
    return bedrock_agent_runtime.retrieve_and_generate(
        input={
            'text': query,
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': kbId,
                'modelArn': modelArn,
            }
        }
    )

def lambda_handler(event, context):
    response = retrieve("중대재해처벌법의 대상이 누구인가요?", "{KnowledgeBaseID}")
    output = response["output"]
    citations = response["citations"]
    
    return output
