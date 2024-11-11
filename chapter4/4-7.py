import boto3

bedrock_agent_runtime = boto3.client(
    service_name = "bedrock-agent-runtime"
)

def retrieve(query, kbId, numberOfResults=5):
    return bedrock_agent_runtime.retrieve(
        retrievalQuery= {
            'text': query
        },
        knowledgeBaseId=kbId,
        retrievalConfiguration= {
            'vectorSearchConfiguration': {
                'numberOfResults': numberOfResults
            }
        }
    )

def lambda_handler(event, context):
    response = retrieve("생애최초 특별공급은 어떻게 신청하나요?", "{KnowledgeBaseID}")
    results = response["retrievalResults"]
    return results
