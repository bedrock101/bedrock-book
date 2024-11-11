import boto3
import re

prompt = """주어진 소설 <novel>을 바탕으로 10개의 질문과 10개의 답변 쌍을 생성해주세요. 각 질문은 소설의 특정 부분이나 세부 정보에 초점을 맞추어야 하며, 전체 내용을 파악할 필요가 없는 것이어야 합니다. 단계별로 생각하고 작성할 질문의 수에 주의를 기울이세요.

<novel>
{소설 원문}
</novel>

지침:
1. 질문은 구체적이고 명확해야 합니다.
2. 답변은 소설 내용에서 직접 추출할 수 있는 정보여야 합니다.
3. 질문은 인물의 이름, 장소, 사건의 날짜, 특정 대화, 물건의 설명 등 구체적인 정보를 묻는 것이어야 합니다.
4. 해석이나 추론이 필요한 질문은 피해주세요.
5. 질문의 답변은 한 문장 또는 간단한 구절로 표현될 수 있어야 합니다.

다음 형식을 사용하여 질문과 답변을 작성해주세요.

Question: [소설의 특정 세부 정보를 묻는 질문]
Answer: [소설에서 직접 추출한 간단하고 명확한 답변]
"""

messages = [{"role": "user", "content": [{"text": prompt}]}]
inference_config = {"temperature": 0.5, "maxTokens": 4096, "topP": 0.9}
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

response = bedrock_runtime.converse(
    modelId="anthropic.claude-3-haiku-20240307-v1:0",
    messages=messages,
    inferenceConfig=inference_config
)

print(response['output']['message']['content'][0]['text'])
result = response['output']['message']['content'][0]['text']

q_pos = [(a.start(), a.end()) for a in list(re.finditer("Question:", result))]
a_pos = [(a.start(), a.end()) for a in list(re.finditer("Answer:", result))]

questions = []
answers = []
for i in range(len(q_pos)):
    q_start = q_pos[i][1]
    q_end = a_pos[i][0] if i < len(a_pos) else None
    a_start = a_pos[i][1]
    a_end = q_pos[i+1][0] if i+1 < len(q_pos) else None
        
    question = result[q_start:q_end].strip()
    answer = result[a_start:a_end].strip()
        
    questions.append(question)
    answers.append(answer)

