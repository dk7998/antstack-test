import os
from typing import Tuple
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
    '''
        A wrapper function to catch any Internal server errors and return 500
    '''
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

def find_meta_tag_value(url: str, name: str) -> Tuple[bool, str]:
    '''
        find_meta_tag_value: finds the meta tag value using python requests and bs4 packages
        :param url(str): URL of a website
        :param name(str): name of the meta tag to find

        return (tuple): [tag exists, tag content] 
    '''
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    meta_tag = soup.find('meta', {'name': name})
    
    if meta_tag:
        return True, meta_tag.get('content')
    else:
        return False, None

def check_dns_txt_record_exists(url: str, txt_record: str) -> bool:
    '''
        check_dns_txt_record_exists: checks whether a txt record exists in the DNS for the given URL
        :param url(str): URL of a website
        :param txt_record(str): TXT record to check

        return (bool): whether txt record exists or not for the given URL

    '''
    url = urlparse(url).netloc
    res = resolver.resolve(url, 'TXT')
    txt_record = f'"{txt_record}"'
    for txt in res:
        if txt.to_text() == txt_record:
            return True
    
    return False

def add_payload_response_to_db(payload: dict, response: dict):
    '''
        add_payload_response_to_db: to add the request payload and response to dynamodb table
        :param payload (dict): request payload
        :param response (dict): response sent by the endpoint 
    '''
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


