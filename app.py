import os
import json
import sys
import boto3

# print("Imported successfully....")

prompt = """
        You are a smart assistant that helps you to order food.

"""

bedrock = boto3.client(service_name="bedrock-runtime")


payload = {

}

body = json.dumps(payload)

model_id = "meta.llama3-8b-instruct-v1:0"

response = bedrock.invoke_model(
    body = body,
    model_id = model_id,
    accept = "application/json",
    content_type="application/json"
)

