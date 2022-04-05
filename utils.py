import os
import uuid
import json
import logging
from functools import wraps
from urllib.parse import urlparse

import requests
import boto3
from dns import resolver
from bs4 import BeautifulSoup


log = logging.getLogger(__name__)


def catch_exception(func):
    @wraps(func)
    def log_and_return_exception(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.exception(e)
            response = {'message': 'An error occured while processing the request!'}
            return {
                'statusCode': 500,
                'body': json.dumps(response)
            }

    return log_and_return_exception

def find_meta_tag_value(url: str, name: str):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    meta_tag = soup.find('meta', {'name': name})
    
    if meta_tag:
        return True, meta_tag.get('content')
    else:
        return False, None

def check_dns_txt_record_exists(url: str, txt_record: str):
    url = urlparse(url).netloc
    res = resolver.resolve(url, 'TXT')
    txt_record = f'"{txt_record}"'
    for txt in res:
        if txt.to_text() == txt_record:
            return True
    
    return False

def add_payload_response_to_db(payload: dict, response: dict):
    session = boto3.Session(os.environ.get('ACCESS_ID'), os.environ.get('SECRET_KEY'))
    dynamo_db = session.resource('dynamodb', os.environ.get('REGION_NAME'))
    requests_table = dynamo_db.Table('Requests')
    # print(requests_table)
    item = {
        'payload': payload,
        'response': response,
        'id': str(uuid.uuid4())
    }

    requests_table.put_item(Item=item)


