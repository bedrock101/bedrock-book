import base64
import json
from pathlib import Path

# 이미지 파일을 Base64 인코딩된 문자열로 변환하는 함수
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 입력 폴더의 이미지들을 처리하여 출력 파일에 JSON 형식으로 저장하는 함수
def process_images(input_folder, input_file):
    input_path = Path(input_folder)
    
    # 출력 파일을 추가 모드로 열고, 반복하여 수행
    with open(input_file, 'a') as file:
        for image_file in input_path.glob('*.jpeg'):
            base64_image = image_to_base64(image_file)
            
            data = {
                "modelInput": {
                    "inputImage": base64_image,
                    "embeddingConfig": {
                        "outputEmbeddingLength": 256
                    }
                }
            }
            file.write(json.dumps(data) + '\n')

process_images('./images', ‘input.jsonl')
