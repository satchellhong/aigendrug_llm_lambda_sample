# src/websocket/default.py
import json
def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Message received on $default route')
    }