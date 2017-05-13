# -*- coding: utf-8 -*-

import json
import boto3

def handler(event, context):
    resp_dict = {}

    if not 'order_id' in event:
        raise Exception('Error')

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PizzaOrder')
    response = table.get_item(
                    Key = {
                        'order_id': event['order_id']
                    }
                )
    item = response['Item']
    resp = {}
    resp['menu_id'] = item['menu_id']
    resp['order_id'] = item['order_id']
    resp['customer_name'] = item['customer_name']
    resp['customer_email'] = item['customer_email']
    resp['order_status'] = item['order_status']


    resp_order = {}
    resp_order['selection'] = item['selection'] 
    resp_order['size'] = item['size']
    resp_order['costs'] = item['costs']
    resp_order['order_time'] = item['order_time']

    resp['order'] = resp_order
    resp_dict['Message'] = resp

    return resp_dict
