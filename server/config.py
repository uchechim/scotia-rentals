from dotenv import load_dotenv
load_dotenv()

import os

# Config class to access all environmental variables (abstracted from public) for this project
class Config:
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = int(os.getenv('DB_PORT', 3306)) #default to 3306 if port for some reason is missing in env
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    SQUARE_ACCESS_TOKEN = os.getenv('SQUARE_ACCESS_TOKEN')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY_ID = os.getenv('AWS_SECRET_ACCESS_KEY_ID')
    AWS_REGION = os.getenv('AWS_REGION')
    AWS_SESSION_TOKEN_ID = os.getenv('AWS_SESSION_TOKEN_ID')
    S3_BUCKET = os.getenv('S3_BUCKET')