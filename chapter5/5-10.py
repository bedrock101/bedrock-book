import boto3
import uuid
import json

bedrock = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-west-2',
)

response = bedrock.invoke_agent(
    inputText="{블로그 글 URL}",
    agentId='AGENT01234',
    agentAliasId='ALIAS0123',
    sessionId=str(uuid.uuid1()),
    enableTrace=True
)

for event in response['completion']:
    if 'chunk' in event:
        data = event['chunk']['bytes']
        answer = data.decode('utf8')
        print(f"Answer:\n{answer}")
    # enableTrace이 False일 경우, 아래 두 행을 삭제합니다.
    elif 'trace' in event:
        print(json.dumps(event['trace'], indent=2))
