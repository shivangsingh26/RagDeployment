import boto3
import os

def get_aws_details():
    session = boto3.session.Session()
    sts = boto3.client('sts')
    
    return {
        'region': session.region_name,
        'account_id': sts.get_caller_identity()['Account'],
        'profile_name': 'llama3-qa-profile'  # Replace with your actual profile name
    }

# Get AWS details
aws_details = get_aws_details()

# Construct the ARN
INFERENCE_PROFILE_ARN = f"arn:aws:bedrock:{aws_details['region']}:{aws_details['account_id']}:inference-profile/{aws_details['profile_name']}"

BEDROCK_CONFIG = {
    "inference_profile_arn": INFERENCE_PROFILE_ARN,
    "model_id": "meta.llama3-1-70b-instruct-v1:0",
    "temperature": 0.7,
    "max_tokens": 2000,
}

# Additional configurations
VECTOR_STORE_CONFIG = {
    "chunk_size": 1000,
    "chunk_overlap": 0,
    "similarity_search_k": 3,
}

# Path configurations
DATA_DIR = "data"
VECTOR_STORE_PATH = "faiss_index"

# Print configuration for verification
if __name__ == "__main__":
    print(f"Region: {aws_details['region']}")
    print(f"Account ID: {aws_details['account_id']}")
    print(f"Profile Name: {aws_details['profile_name']}")
    print(f"Full ARN: {INFERENCE_PROFILE_ARN}")