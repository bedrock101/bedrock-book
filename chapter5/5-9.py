import json
import urllib.request
from bs4 import BeautifulSoup 
import html

def get_article_text(url: str) -> str:
    if any(ord(char) > 127 for char in url):
        encoded_url = urllib.parse.quote(url, safe=':/?=&@')
    else:
        encoded_url = url
        
    req = urllib.request.Request(encoded_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as response:
        html_doc = response.read()
    
    decoded_html = html.unescape(html_doc.decode('utf-8'))
    soup = BeautifulSoup(decoded_html, 'html.parser')
    
    for style in soup(["style"]):
        style.decompose()
        
    # 모든 요소 내, 텍스트 추출
    text_content = u''.join(soup.findAll(string=True))

    # 연속된 공백 제거
    text = ' '.join(text_content.split())
    
    return text

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    if function == 'evaluate_article':
        url = next((item['value'] for item in event['parameters'] if item['name'] == 'url'), '')
        body = {'body': get_article_text(url)}

    responseBody = {
        "TEXT": {
            "body": json.dumps(body, ensure_ascii=False)
        }
    }
    
    action_response = {
        'actionGroup': event['actionGroup'],
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }
    }
    
    return {
        'messageVersion': '1.0',
        'response': action_response
    }
