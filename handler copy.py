import json
import boto3
import os

from botocore.exceptions import ClientError

def main(event, context):
    connection_id = event['requestContext']['connectionId']
    domain_name = event['requestContext']['domainName']
    stage = event['requestContext']['stage']
    endpoint = f"https://{domain_name}/{stage}"
    client_api = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint)
    
    # Parse the incoming message body
    try:
        body = json.loads(event['body'])
        user_input = body['data']['target']
    except (KeyError, json.JSONDecodeError):
        error_message = "Invalid input format. Please provide a 'target' field."
        client_api.post_to_connection(ConnectionId=connection_id, Data=json.dumps({"error": error_message}))
        return {'statusCode': 400, 'body': json.dumps({"error": error_message})}
    
    # Create a Bedrock Runtime client in the AWS Region you want to use.
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    
    # Set the model ID
    model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    # Define the prompt for the model using the user's input
    prompt = f"Give me the {user_input} targeting approved drug list including the approval years, own company, and drug type with json format."
    
    # Format the request payload using the model's native structure.
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        streaming_response = client.invoke_model_with_response_stream(
            modelId=model_id, body=request
        )
      
    except (ClientError, Exception) as e:
        error_message = f"ERROR: Can't invoke '{model_id}'. Reason: {str(e)}"
        print(error_message)
        client_api.post_to_connection(ConnectionId=connection_id, Data=json.dumps({"error": error_message}))
        return {'statusCode': 500, 'body': json.dumps({"error": error_message})}
    
    # Extract and send the response text in real-time.
    for event in streaming_response["body"]:
        chunk = json.loads(event["chunk"]["bytes"])
        if chunk["type"] == "content_block_delta":
            data = chunk["delta"].get("text", "") 
            print(data, end="")
            client_api.post_to_connection(ConnectionId=connection_id, Data=data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data sent in chunks')
    }