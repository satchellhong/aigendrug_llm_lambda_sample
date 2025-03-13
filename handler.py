import json
import boto3
import os
from botocore.exceptions import ClientError
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_aws import ChatBedrock
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

from src.connection import send_to_connection

# Initialize global variables to maintain state across Lambda invocations
vector_store = None
chain = None


def initialize_rag():
    """Initialize RAG components if not already initialized"""
    global vector_store, chain

    if vector_store is None:
        # Initialize Bedrock client
        bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

        # Initialize embeddings
        bedrock_embeddings = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v2:0", client=bedrock
        )

        # Load the vector store
        vector_store = FAISS.load_local(
            "faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True
        )

        # Initialize LLM
        llm = ChatBedrock(
            model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
            client=bedrock,
            streaming=True,
            model_kwargs={
                "max_tokens": 1000,
                "temperature": 0,
                "top_p": 1,
                "top_k": 250,
                "anthropic_version": "bedrock-2023-05-31",
            },
        )

        # Set up prompt template
        prompt = PromptTemplate.from_template(
            """You are an expert assistant for chemical analysis and drug development tasks.
            Use the following pieces of retrieved context to answer the question.
            If you don't know the answer, just say that you don't know.
            Provide one specific recommendation for the given task, explaining why it's the best choice.
            Conclude your answer with: "Would you like to run the tool <tool name>?"

            Question: {question}
            Context: {context}
            Answer:"""
        )

        # Set up retriever and chain
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        chain = (
            {
                "context": retriever,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

def main(event, context):
    # Extract WebSocket connection details
    connection_id = event["requestContext"]["connectionId"]
    domain_name = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    endpoint = f"https://{domain_name}/{stage}"

    # Parse the incoming message body
    try:
        body = json.loads(event["body"])
        user_input = body["data"][
            "question"
        ]  # Changed from 'target' to 'question' to match RAG use case
    except (KeyError, json.JSONDecodeError):
        error_message = "Invalid input format. Please provide a 'question' field."
        send_to_connection(
            connection_id, json.dumps({"error": error_message}), endpoint
        )
        return {"statusCode": 400, "body": json.dumps({"error": error_message})}

    try:
        # Initialize RAG components if needed
        initialize_rag()

        # Stream the response
        for chunk in chain.stream(user_input):
            send_to_connection(connection_id, chunk, endpoint)

        return {
            "statusCode": 200,
            "body": json.dumps("Streaming completed successfully"),
        }

    except Exception as e:
        error_message = f"Error processing request: {str(e)}"
        send_to_connection(
            connection_id, json.dumps({"error": error_message}), endpoint
        )
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}
