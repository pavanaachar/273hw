# -*- coding: utf-8 -*-

import boto3
import json
from botocore.exceptions import ClientError

def handler(event, context):
    table = boto3.resource('dynamodb', region_name='us-west-2').Table('PizzaMenu')
    try:
        table.put_item(Item={"menu_id": event["menu_id"],
                             "selection" : event["selection"]
                               })
    except Exception, e:
        raise Exception("Error: %s" % e.message)
    return "OK"
