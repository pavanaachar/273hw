# -*- coding: utf-8 -*-

import boto3
import json
from botocore.exceptions import ClientError

def handler(event, context):
    resp_dict = {}
    order_table = boto3.resource('dynamodb', region_name='us-west-2').Table('PizzaOrder')
    menu_table = boto3.resource('dynamodb', region_name='us-west-2').Table('PizzaMenu')
    try:
        order_table.put_item(Item={'order_id': event['order_id'],
                             'menu_id': event['menu_id'],
                             'customer_name' : event['customer_name'],
                             'customer_email': event['customer_email'],
                             'size': 'null',
                             'selection': 'null',
                             'order_time': 'null',
                             'order_status': 'null',
                             'costs': 'null'
                             })
        response = menu_table.get_item(Key = {
                                         'menu_id': event['menu_id']
                                         })
        item = response['Item']
        selection = item['selection']
        message = "Hi "+ event["customer_name"] + ", please choose one of these selection: "
        for i in range(1, len(selection)+1):
            message += str(i) + ". " + selection[i-1]
            if i < len(selection):
               message += ', '  
        resp_dict['message'] = message

    except Exception, e:
        raise Exception("Error: %s" % e.message)
    return resp_dict
