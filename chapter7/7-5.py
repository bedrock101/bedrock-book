import ragas
from langchain_aws import BedrockEmbeddings
from langchain_aws import ChatBedrock
from datasets import Dataset

df['contexts'] = df['retrieved_doc_texts'].apply(lambda x: x if isinstance(x, list) else [x])
df['ground_truths'] = df['gt_answers'].apply(lambda x: [x])
df['reference'] = df['contexts'].apply(lambda x: ' '.join(x))

ragas_result = ragas.evaluate(
    Dataset.from_pandas(df),
    metrics=[
        ragas.metrics.answer_relevancy,
        ragas.metrics.faithfulness,
        ragas.metrics.context_precision,
        ragas.metrics.context_recall,
        ragas.metrics.answer_similarity,
        ragas.metrics.answer_correctness
    ],
    llm=ChatBedrock(model_id="anthropic.claude-3-sonnet-20240229-v1:0"),
    embeddings=BedrockEmbeddings(model_id="cohere.embed-multilingual-v3"),
    column_map={
        "answer": "model_answer",
        "contexts": "contexts",
        "ground_truths": "ground_truths",
        "question": "question",
        "reference": "reference",
    }
)
