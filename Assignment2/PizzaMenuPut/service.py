# -*- coding: utf-8 -*-

import boto3
import json
from botocore.exceptions import ClientError

def update_item(table, key_name, key_val, attr_name, attr_val):
    table.update_item(
                      Key = {
                          key_name: key_val,
                      },
                      UpdateExpression='SET ' + attr_name + ' = :val1',
                      ExpressionAttributeValues={
                          ':val1': attr_val
                      })

def handler(event, context):
    table = boto3.resource('dynamodb', region_name='us-west-2').Table('PizzaMenu')
    try:
        update_item(table=table,
                    key_name = "menu_id",
                    key_val = event["menu_id"],
                    attr_name = "selection",
                    attr_val = event["selection"]
                   )

    except Exception, e:
        raise Exception("Error: %s" % e.message)
    return "OK"
