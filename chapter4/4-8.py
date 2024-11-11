import boto3

bedrock_agent_runtime = boto3.client(
    service_name = "bedrock-agent-runtime"
)

def retrieve(query, kbId):
    modelArn = 'arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-v2:1'
    
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
    response = retrieve("생애최초 특별공급은 어떻게 신청하나요?", "{KnowledgeBaseID}")
    output = response["output"]
    citations = response["citations"]
    
    return output
