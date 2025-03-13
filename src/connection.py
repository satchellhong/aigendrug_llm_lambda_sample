import boto3
from botocore.exceptions import ClientError

def send_to_connection(connection_id, data, endpoint):
    """Helper function to send data to WebSocket connection"""
    client = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint)
    try:
        client.post_to_connection(ConnectionId=connection_id, Data=data)
    except ClientError as e:
        print(f"Error sending message: {str(e)}")
        return False
    return True