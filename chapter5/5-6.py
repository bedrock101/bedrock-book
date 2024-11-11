import logging, json, boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_qr_code(url, size=6, transparent=False):
    base_url = "https://qrtag.net/api/qr"

    if transparent:
        base_url += "_transparent"
    
    qr_url = f"{base_url}_{size}.png?url={url}"
    
    return qr_url
    
def generate_text(bedrock_client, model_id, tool_config, input_text):
    """제공된 Amazon Bedrock 모델을 사용하여 텍스트를 생성합니다.
    필요한 경우, 이 함수는 도구 사용 요청을 처리하고 그 결과를 모델에 전송합니다."""

    logger.info("Generating text with model %s", model_id)

    messages = [{
        "role": "user",
        "content": [{"text": input_text}]
    }]

    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        toolConfig=tool_config
    )

    output_message = response['output']['message']
    messages.append(output_message)
    stop_reason = response['stopReason']

    if stop_reason == 'tool_use':
        tool_requests = response['output']['message']['content']
        for tool_request in tool_requests:
            if 'toolUse' in tool_request:
                tool = tool_request['toolUse']
                logger.info("Requesting tool %s. Request: %s",
                            tool['name'], tool['toolUseId'])

                if tool['name'] == 'generate_qr':
                    tool_result = {}
                    try:
                        qr_url = generate_qr_code(
                            tool['input']['url'],
                            tool['input'].get('size', 6),
                            tool['input'].get('transparent', False)
                        )
                        tool_result = {
                            "toolUseId": tool['toolUseId'],
                            "content": [{"text": f"QR code generated: {qr_url}"}]
                        }
                    except Exception as err:
                        tool_result = {
                            "toolUseId": tool['toolUseId'],
                            "content": [{"text": str(err)}],
                            "status": 'error'
                        }

                    tool_result_message = {
                        "role": "user",
                        "content": [
                            {
                                "toolResult": tool_result
                            }
                        ]
                    }
                    messages.append(tool_result_message)

                    response = bedrock_client.converse(
                        modelId=model_id,
                        messages=messages,
                        toolConfig=tool_config
                    )
                    output_message = response['output']['message']

    for content in output_message['content']:
        print(json.dumps(content, indent=4))

def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    input_text = "https://heuristicwave.github.io 주소로 QR을 생성해줘 투명한 배경으로 사이즈는 4로 해줘"

    tool_config = {
    "tools": [
        {
            "toolSpec": {
                "name": "generate_qr",
                "description": "주어진 URL로 부터 QR code 생성.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "QR code로 변경할 URL"
                            },
                            "size": {
                                "type": "integer",
                                "description": "QR code 이미지의 크기 (옵션, 기본값 6)."
                            },
                            "transparent": {
                                "type": "boolean",
                                "description": "투명한 QR code 생성 여부 (옵션, 기본값 false)."
                            }
                        },
                        "required": [
                            "url"
                        ]
                    }
                }
            }
        }
    ]
}
    bedrock_client = boto3.client(service_name='bedrock-runtime')

    try:
        print(f"Request: {input_text}")
        generate_text(bedrock_client, model_id, tool_config, input_text)

    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        print(f"A client error occurred: {message}")

    else:
        print(f"Finished generating text with model {model_id}.")

if __name__ == "__main__":
    main()
