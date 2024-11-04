import boto3
import json

def verify_bedrock_setup():
    try:
        # Create Bedrock client
        bedrock = boto3.client('bedrock')
        
        # List available models
        response = bedrock.list_foundation_models()
        
        print("\nAvailable Models:")
        for model in response['modelSummaries']:
            print(f"\nModel ID: {model['modelId']}")
            print(f"Provider: {model['providerName']}")
            
        # List inference profiles
        profiles = bedrock.list_inference_profiles()
        
        print("\nExisting Inference Profiles:")
        for profile in profiles.get('inferenceProfiles', []):
            print(f"\nProfile Name: {profile['name']}")
            print(f"Profile ARN: {profile['arn']}")
            print(f"Model ID: {profile['modelId']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nPlease check:")
        print("1. AWS credentials are properly configured")
        print("2. Your IAM role/user has necessary Bedrock permissions")
        print("3. Bedrock service is enabled in your AWS account")
        print("4. You're in a region where Bedrock is available")

if __name__ == "__main__":
    verify_bedrock_setup()