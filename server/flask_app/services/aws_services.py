import boto3
import json

#as the application scales, i might utilize different config files (developmentConfig, testingConfig e.t.c) 
#current_app just ensures that I am using the config defined on creating the application
from flask import make_response 
from config import Config


aws_access_key_id = Config.AWS_ACCESS_KEY_ID
aws_secret_access_key_id = Config.AWS_SECRET_ACCESS_KEY_ID
aws_session_token_id = Config.AWS_SESSION_TOKEN_ID
region_name = Config.AWS_REGION

s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, 
                  aws_secret_access_key=aws_secret_access_key_id, 
                  aws_session_token=aws_session_token_id, 
                  region_name=region_name)

s3_bucket = Config.S3_BUCKET

aws_secrets_manager_client = boto3.client('secretsmanager', 
                                          aws_access_key_id=aws_access_key_id, 
                                          aws_secret_access_key=aws_secret_access_key_id, 
                                          aws_session_token=aws_session_token_id, 
                                          region_name=region_name)

def get_user_auth_secret(user_email):
    try:
        response = aws_secrets_manager_client.get_secret_value(SecretId=user_email)
        user_secret_payload = json.loads(response['SecretString'])

        return user_secret_payload
    except:
        return make_response({'error message': 'There was an error retrieving the aws secret value for user: {email}'.format(email=user_email)}, 400)

def create_user_auth_secret(user_email, encrypted_password):

    try:
        secret_payload = {
            "email": user_email,
            "password": encrypted_password
        }

        aws_secrets_manager_client.create_secret(Name=user_email, SecretString=json.dumps(secret_payload))
        return make_response({'success message': 'Successfully created an aws secret for user: {email}'.format(email=user_email)}, 200)
    except:
        return make_response({'error message': 'Error creating an aws secret for user: {email}'.format(email=user_email)}, 400)


def list_s3_objects():
    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket)

        if 'Contents' in response:
            return response['Contents']
        else:
            return make_response({'Empty Bucket Err Message': 'The S3 bucket: {bucket_name} is empty: []'.format(bucket_name=s3_bucket)}, 400)
    except:
        return make_response({'error message': 'Error listing S3 bucket object for bucket: {bucket_name}'.format(bucket_name=s3_bucket)}, 400)
        
    




