# CodeLlama 모델을 로컬로 복제
git clone https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf

# 로컬에 클론 받은 파일을 S3 버킷에 업로드
aws s3 cp ./CodeLlama-7b-Instruct-hf/ s3://{YOUR BUCKET NAME}/{PATH} --recursive
