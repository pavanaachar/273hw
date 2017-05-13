# -*- coding: utf-8 -*-

import json
import boto3

def handler(event, context):
    if not 'menu_id' in event:
        raise Exception('Error: Menu id required')

    # Get the service resource.
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('PizzaMenu')
        response = table.delete_item(
                        Key = {
                            'menu_id': event['menu_id']
                        }
                    )
    except Exception as e:
        return "Error deleting the menu: %s" % e.message
    return "OK"
