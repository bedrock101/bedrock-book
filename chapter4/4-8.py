import boto3

bedrock_agent_runtime = boto3.client(service_name = "bedrock-agent-runtime")

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
    response = retrieve("중대재해처벌법의 대상이 누구인가요?", "{KnowledgeBaseID}")
    results = response["retrievalResults"]
    return results
