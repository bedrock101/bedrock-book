from langchain_aws import ChatBedrockConverse
from langchain_aws import BedrockEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector

llm = ChatBedrockConverse(model="anthropic.claude-3-5-sonnet-20240620-v1:0")
embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")

loader = WebBaseLoader("https://aws.amazon.com/bedrock/titan/")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

connection = "postgresql+psycopg://postgres:pgvector@pgvector2.cluster-example12345.ap-northeast-2.rds.amazonaws.com:5432/postgres"
collection_name = "aws_vector"

vectordb = PGVector.from_documents(
    documents=splits,
    embedding=embeddings,
    connection_string=connection,
    collection_name=collection_name,
    use_jsonb=True,
)

prompt_template = """
    마지막에 질문에 대한 간결한 답변을 제공하기 위해 다음 문맥을 활용하세요.
    답을 모른다면 답을 지어내려고 하지 말고 모른다고 말하세요.
    
    <context>
    {context}
    </context>

    Question: {question}
"""

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {
        "context": vectordb.as_retriever() | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

answer=rag_chain.invoke("Titan Embedding V2는 몇 차원인가요?")
print(answer)
