import json
import boto3
import csv
from io import StringIO

s3 = boto3.resource("s3")

def lambda_handler(event, context):
    bucket = s3.Bucket(event["bucketName"])

    response_event = {"outputFiles": []}

    for file in event["inputFiles"]:
        output_file = {
            "originalFileLocation": file["originalFileLocation"],
            "fileMetadata": file.get("fileMetadata", {}),
            "contentBatches": [],
        }
        response_event["outputFiles"].append(output_file)

        for n, content in enumerate(file["contentBatches"]):
            content_input_key = content["key"]
            content_object = bucket.Object(content_input_key)

            content_text = content_object.get()["Body"].read().decode("utf-8")
            content_json = json.loads(content_text)

            print(content_json)

            output_file_content = []
            for file_content in content_json["fileContents"]:
                body = file_content["contentBody"]
                
                # CSV 파일을 행별로 처리
                csv_reader = csv.reader(StringIO(body))
                for row in csv_reader:
                    output_file_content.append({
                        "contentMetadata": file_content["contentMetadata"],
                        "contentBody": ",".join(row), 
                        "contentType": file_content["contentType"],
                    })

            output = {"fileContents": output_file_content}

            content_output_key = f"{content_input_key}_out_{n}"
            content_output_object = bucket.Object(content_output_key)

            content_output_object.put(
                Body=json.dumps(output).encode("utf-8"),
                ContentEncoding="utf-8",
                ContentType="application/json",
            )

            output_file["contentBatches"].append({"key": content_output_key})

    return response_event
