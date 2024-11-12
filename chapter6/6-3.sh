# Llama-3.2-3B-Instruct 모델을 로컬로 복제 
git clone https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct

# 로컬에 클론 받은 파일을 S3 버킷에 업로드
aws s3 cp ./Llama-3.2-3B-Instruct/ s3://{YOUR BUCKET NAME}/{PATH} --recursive
