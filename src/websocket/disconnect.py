# src/websocket/disconnect.py
def handler(event, context):
    try:
        return {'statusCode': 200, 'body': 'Disconnected with DrugVLAB ChatBot.'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}