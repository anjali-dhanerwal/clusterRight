"""
AWS Session Utilities

Helper functions for generating and managing AWS session tokens
"""

import os
import logging
import boto3
from dotenv import load_dotenv

# Suppress logging
for logger_name in ['botocore', 'boto3', 'urllib3']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)


def get_session_token(duration_seconds=3600):
    """
    Generate a temporary session token using AWS STS
    
    Args:
        duration_seconds (int): Token validity duration (1-43200 seconds, default 1 hour)
    
    Returns:
        dict: Credentials dictionary with AccessKeyId, SecretAccessKey, SessionToken
    """
    try:
        # Load environment variables
        load_dotenv()
        print (os.getenv("AWS_ACCESS_KEY_ID"))
        # Create STS client
        sts_client = boto3.client(
            'sts',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        
        # Get session token
        response = sts_client.get_session_token(DurationSeconds=duration_seconds)
        
        return response['Credentials']
        
    except Exception as e:
        print(f"Error generating session token: {e}")
        return None

def refresh_session_token_in_env():
    """
    Generate a new session token and update environment variables
    
    Returns:
        bool: True if successful, False otherwise
    """
    credentials = get_session_token()
    
    if credentials:
        # Update environment variables
        os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
        os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
        os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']
        
        print(f"✅ Session token refreshed. Expires: {credentials['Expiration']}")
        return True
    
    return False

def get_caller_identity():
    """
    Get information about the current AWS identity
    Useful for verifying credentials are working
    """
    try:
        sts_client = boto3.client('sts')
        response = sts_client.get_caller_identity()
        
        print(f"User ID: {response.get('UserId')}")
        print(f"Account: {response.get('Account')}")
        print(f"ARN: {response.get('Arn')}")
        
        return response
        
    except Exception as e:
        print(f"Error getting caller identity: {e}")
        return None