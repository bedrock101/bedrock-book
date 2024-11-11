from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import boto3
from tqdm.auto import tqdm

def retrieve_and_generate(
    question: str,
    kb_id: str,
    generate_model_arn: str = f"arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
):
    bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-west-2")
    rag_resp = bedrock_agent.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": kb_id,
                "modelArn": generate_model_arn,
                'generationConfiguration': {
                    'inferenceConfig': {
                        'textInferenceConfig': {
                            'maxTokens': 256,
                        }
                    }
                }
            },
            "type": "KNOWLEDGE_BASE",
        },
    )
    all_refs = [r for cite in rag_resp["citations"] for r in cite["retrievedReferences"]]
    ref_s3uris = [r["location"]["s3Location"]["uri"] for r in all_refs]
 
    ref_ids = [uri.rpartition("/")[2].rpartition(".")[0] for uri in ref_s3uris]
    return {
        "answer": rag_resp["output"]["text"],
        "retrieved_doc_texts": [r["content"]["text"] for r in all_refs]
    }

# 질문과 답변으로 DataFrame 생성
df = pd.DataFrame({'question': questions, 'gt_answers': answers})

# ThreadPoolExecutor를 사용하여 비동기적으로 RAG 호출
with ThreadPoolExecutor(max_workers=5) as executor:
    # Future 객체와 원래 인덱스를 함께 저장
    future_to_index = {executor.submit(retrieve_and_generate, question=q, kb_id="7VJRQS0P7S"): i 
                       for i, q in enumerate(df['question'])}
    
    results = [None] * len(df)  
    for future in tqdm(as_completed(future_to_index), total=len(future_to_index), desc="Running RAG..."):
        index = future_to_index[future]
        results[index] = future.result()

# 결과를 DataFrame에 추가
df['model_answer'] = [r['answer'] for r in results]
df['retrieved_doc_texts'] = [r['retrieved_doc_texts'] for r in results]
