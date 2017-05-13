# -*- coding: utf-8 -*-

import json
import boto3

def handler(event, context):
    resp_dict = {}

    if not 'menu_id' in event:
        raise Exception('Error')

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PizzaMenu')
    response = table.get_item(
                    Key = {
                        'menu_id': event['menu_id']
                    }
                )

    item = response['Item']

    return item
