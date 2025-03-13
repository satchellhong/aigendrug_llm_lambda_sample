# src/websocket/connect.py
def handler(event, context):
    try:
        return {"statusCode": 200, "body": "Connected to DrugVLAB ChatBot."}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
