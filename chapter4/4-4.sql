CREATE SCHEMA bedrock_integration;

CREATE ROLE bedrock_user WITH PASSWORD 'yourpassword' LOGIN;

GRANT ALL ON SCHEMA bedrock_integration to bedrock_user;
