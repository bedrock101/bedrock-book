import fitz
import json

doc = fitz.open("{파일명}.pdf")
output_file = "input.jsonl"

with open(output_file, "w", encoding="utf-8") as jsonl_file:
    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()  # 블록의 텍스트 내용을 가져오고 앞뒤 공백 제거
            if len(text) >= 8:       # 텍스트 길이가 8 이상인 경우에만 처리
                json_object = {"input": text}
                json_line = json.dumps(json_object, ensure_ascii=False)
                jsonl_file.write(json_line + "\n")

print(f"JSONL 파일이 생성되었습니다: {output_file}")
