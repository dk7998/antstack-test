import json

from marshmallow import ValidationError

from schema import MetaTagRequestSchema, DNSTxtCheckSchema
from utils import find_meta_tag_value, check_dns_txt_record_exists, catch_exception, add_payload_response_to_db


@catch_exception
def get_meta_tag_value(event, context):
    '''
        An endpoint to get meta tag value by name from a website
    '''
    schema = MetaTagRequestSchema()
    ip_data = event.get('queryStringParameters', {})
    try:
        data = schema.load(ip_data)
    except ValidationError as err:
        response = {
            'statusCode': 400,
            'body': json.dumps(err.messages)
        }
    else:        
        tag_present, content = find_meta_tag_value(data['url'], data['meta_tag_name'])
        response =  {
            'statusCode': 200,
            'body': json.dumps({
                    'tag_present': tag_present,
                    'content': content
                })
            }
    
    add_payload_response_to_db(ip_data, response)        
    return response

@catch_exception
def check_dns_txt(event, context):
    '''
        An endpoint to check the TXT record in DNS
    '''
    schema = DNSTxtCheckSchema()
    ip_data = json.loads(event.get('body', '{}'))
    try:
        data = schema.load(ip_data)
    except ValidationError as err:
        response =  {
            'statusCode': 400,
            'body': json.dumps(err.messages)
        }
    else:
        txt_exists = check_dns_txt_record_exists(data['url'], data['txt_record'])
        response = {
            'statusCode': 200,
            'body': json.dumps({'txt_record_exists': str(txt_exists)})
        }

    add_payload_response_to_db(ip_data, response)
    return response