import json

import boto3

import datetime

def updateItem(table, key_name, key_val, attr_name, attr_val):
    table.update_item(
        Key = {
            key_name: key_val,
        },
        UpdateExpression='SET ' + attr_name + ' = :val1',
        ExpressionAttributeValues={
            ':val1': attr_val
        }
    )

def handler(event, context):
    resp_dict = {}

    dynamodb = boto3.resource('dynamodb')
    
    order_table = dynamodb.Table('PizzaOrder')

    if all(name in event for name in ('input', 'order_id')):
        inputIdx = int(event['input']) - 1
        response = order_table.get_item(
                        Key = {
                            'order_id': event['order_id']
                        }
                    )
        order_item = response['Item']
        menu_id = order_item['menu_id']
        menu_table = dynamodb.Table('PizzaMenu')
        menu_table_response = menu_table.get_item(
                                    Key = {
                                        'menu_id': menu_id
                                    }
                                )

        menu_item = menu_table_response['Item']
        size = menu_item['size']
        sequence  = menu_item['sequence']
        opId = -1
        for i in range(len(sequence)):
            if order_item[sequence[i]] == 'null':
                if sequence[i] == 'selection':
                    rsp_str =  "Which size do you want? " 
                    for i in range(1, len(size)+1):
                        rsp_str += str(i) + ". " + size[i-1]
                        if i < len(size):
                            rsp_str += ', '
                    resp_dict['Message'] = rsp_str
                    updateItem(table=order_table,
                                key_name='order_id',
                                key_val=event['order_id'],
                                attr_name='selection',
                                attr_val=menu_item['selection'][inputIdx])
                    opId = i
                    break

                elif sequence[i] == 'size':
                    costs = menu_item['price'][inputIdx]
                    resp_str = "Your order costs $" + costs + ". We will email you when the order is ready. Thank you!"
                    resp_dict['Message'] = resp_str
                    updateItem(table=order_table,
                                key_name='order_id',
                                key_val=event['order_id'],
                                attr_name='size',
                                attr_val=menu_item['size'][inputIdx])

                    updateItem(table=order_table,
                                key_name='order_id',
                                key_val=event['order_id'],
                                attr_name='costs',
                                attr_val=costs)

                    opId = i

                    break

                else:
                    raise Exception('Error')


        # Update order timestamp and status on last 'input'
        if opId != -1 and opId == len(sequence)-1:
            # Update order status as 'processing'
            updateItem(table=order_table,
                        key_name='order_id',
                        key_val=event['order_id'],
                        attr_name='order_status',
                        attr_val='processing')

            # Update order timestamp

            ts = datetime.datetime.now().strftime('%m-%d-%Y@%H-%M-%S')
            updateItem(table=order_table,
                        key_name='order_id',
                        key_val=event['order_id'],
                        attr_name='order_time',
                        attr_val=ts)
            response = order_table.get_item(
                            Key = {
                                'order_id': event['order_id']
                            }
                        )
             
    else:
        raise Exception('Error')

    return resp_dict
