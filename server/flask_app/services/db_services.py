import pymysql
import os
from config import Config

def connect_to_aws_db():
    return pymysql.connect(host=Config.DB_HOST, 
                           port=Config.DB_PORT, 
                           user=Config.DB_USER, 
                           password=Config.DB_PASSWORD, 
                           db=Config.DB_NAME       
    )


#add functions related to DB Queries here if needed