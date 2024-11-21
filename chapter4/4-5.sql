CREATE TABLE bedrock_integration.bedrock_kb (id uuid PRIMARY KEY, embedding vector(1024), chunks text, metadata json);

CREATE INDEX on bedrock_integration.bedrock_kb USING hnsw (embedding vector_cosine_ops);

GRANT ALL ON bedrock_integration.bedrock_kb TO bedrock_user;
