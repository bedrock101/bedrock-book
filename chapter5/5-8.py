import json
import urllib.request
from bs4 import BeautifulSoup 
import html

def get_article_body(url: str) -> str:
    encoded_url = urllib.parse.quote(url, safe=':/?=&')
    req = urllib.request.Request(encoded_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html_doc = response.read()
    decoded_html = html.unescape(html_doc.decode('utf-8'))
    soup = BeautifulSoup(decoded_html, 'html.parser')
    for style in soup(["style"]):
        style.decompose()
    texts = soup.stripped_strings
    text = '\n'.join(texts)
    
    return text

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    if function == 'evaluate_article':
        url = next((item['value'] for item in event['parameters'] if item['name'] == 'url'), '')
        body = {'body': get_article_body(url)}

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
