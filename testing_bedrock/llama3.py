import os
import json
import sys
import boto3

# print("Imported successfully....")

prompt1 = """
        You are a smart assistant that helps you to order food.

"""

prompt="""
    You are a cricket expert, can you tell me whether Virat Kohli is overrated.

"""

bedrock = boto3.client(service_name="bedrock-runtime")


payload = {
    "prompt": "[INST]" + prompt + "[/INST]",
    "max_gen_len" : 512,
    "temperature" : 0.5,
    "top_p" : 0.9
}

body = json.dumps(payload)

model_id = "meta.llama3-8b-instruct-v1:0"

response = bedrock.invoke_model(
    body = body,
    modelId = model_id,
    accept = "application/json",
    contentType="application/json"
)

response_body = json.loads(response.get("body").read())
response_text = response_body["generation"]

print(response_text)