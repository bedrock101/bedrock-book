import json
import os

def process_folder(input_folder, output_file, image_ref_prefix):
    # 출력 JSONL 파일 열기
    with open(output_file, 'w', encoding='utf-8') as out_f:
        # 입력 폴더 내의 모든 JSON 파일 처리
        for filename in os.listdir(input_folder):
            if filename.endswith('.json'):
                file_path = os.path.join(input_folder, filename)
                
                # JSON 파일 읽기
                with open(file_path, 'r', encoding='utf-8') as in_f:
                    data = json.load(in_f)
                
                # 새로운 JSONL 데이터 생성
                new_data = {
                    "image-ref": f"{image_ref_prefix}/{os.path.basename(data['meta']['dataset']['source_path'])}",
                    "caption": data['caption']
                }
                
                # JSONL 파일에 데이터 쓰기
                json.dump(new_data, out_f, ensure_ascii=False)
                out_f.write('\n')

    print(f"JSONL 파일이 생성되었습니다: {output_file}")

# 훈련용 데이터 처리
train_input_folder = './Webtoon/Training/Label/Sports'
train_output_file = 'train_output.jsonl'
train_image_ref_prefix = 's3://{YOUR BUCKET NAME}/Webtoon/Training/Raw/Sports'

process_folder(train_input_folder, train_output_file, train_image_ref_prefix)

# 검증용 데이터 처리
val_input_folder = './Webtoon/Validation/Label/Sports'
val_output_file = 'val_output.jsonl'
val_image_ref_prefix = 's3://{YOUR BUCKET NAME}/Webtoon/Validation/Raw/Sports'

process_folder(val_input_folder, val_output_file, val_image_ref_prefix)
