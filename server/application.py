from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask import request  
import pymysql
import random
import boto3
import logging
import hashlib
import json
from square.client import Client


#define flask app and enable cors (cross-browser requests)
application = Flask(__name__)
CORS(application)

#define sql connection with AWS RDS -> MIGHT NEED TO REFACTOR AFTER APPLYING VPC & EC2 E.T.C

db_host = 'scotia-rental-db.claumo22iofg.us-east-1.rds.amazonaws.com'
db_port = 3306
db_user = 'admin'
db_password = 'Asdasdasd1!'
db_name = 'scotiaRentalDB'

db_conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db_name)
unique_user_ids = set()

aws_access_key_id_val ='AKIAU6GDVWXLBIY6YJVU'
region_name_val='us-east-1'
aws_secret_access_key_val = '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'
aws_session_token_val= ''

access_token = "EAAAl2qpBqc0Z0NpqpvpwHhdLZmAUxvwIntE_Vuxwn3xbWGbqeHCFLGPwWAw3oty" #applications access token
square_client = Client(access_token=access_token, environment='sandbox')

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id_val, aws_secret_access_key=aws_secret_access_key_val, aws_session_token=aws_session_token_val, region_name=region_name_val)

aws_secrets_client = boto3.client('secretsmanager', aws_access_key_id=aws_access_key_id_val, aws_secret_access_key=aws_secret_access_key_val, aws_session_token=aws_session_token_val, region_name=region_name_val)



                                                            #******backend routes******
@application.route("/signin", methods=["POST"])
def signin():
    #query database and try to find user.
    #if user exists return corresponding data + JWT token 
    #else, return 400 http status code

    cur = db_conn.cursor()
    data = request.get_json()


    use_stmt = ("USE scotiaRentalDB")

    cur.execute(use_stmt)
 

    cur.execute("SELECT * FROM USER")
    query_details = cur.fetchall()
    
    #retrieve encrypted pw in aws secret manager don't need to do hashing again
    email = data['email']
    password = data['password']

    sha256_password = hashlib.sha256(password.encode())
    encrypted_user_password = sha256_password.hexdigest()


    response = aws_secrets_client.get_secret_value(SecretId=email)
    db_secrets = json.loads(response['SecretString'])
    encrypted_aws_password = db_secrets['password']

    for det in query_details:
        #check if the encrypted user's password (det[4]) == password stored in aws_secrets_manager AND encrypted user pw =aws secrets password
        if det[1] == email and encrypted_user_password == encrypted_aws_password and encrypted_user_password == det[4]:
            user = {'id':det[0], 'firstName':det[1],
                    'lastName':det[2],'email':det[3],
                    'password':det[4],'accountType':det[5],
                    'isAuthenticated':det[6],'userToken':det[7]}
            
            return make_response({'message': "Successfully Signed In", 'user': user}, 200)

    return make_response({'message': "Invalid Credentials"}, 400)

@application.route("/signup", methods=["POST"])
def signup():
    #queries db to find if there is a row/user exists with request.data.email, if not:
    #insert record into table       
    #return correct JSON status 200 if record successfully inserted
    #if a user exists, return 400
    
    cur = db_conn.cursor()
    data = request.get_json()

    use_stmt = ("USE scotiaRentalDB")

    cur.execute(use_stmt)
    insert_stmt = (
    "INSERT INTO USER (UserId, Email, FirstName, LastName, Password, AccountType, IsAuthenticated, Token) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    )

    #setting up data to be inserted into DB
    #reference -> https://stackoverflow.com/questions/72926478/how-do-you-auto-generate-a-random-id-for-an-sqlite-database-table
    rand_id = random.randint(10000000, 99999999) #generates random 8 digit number
    if rand_id in unique_user_ids:
        rand_id = random.randint(10000000, 99999999)
        
    email = data['email']
    firstName = data['firstName']
    lastName = data['lastName']
    password = data['password']
    accountType = data['accountType']

    
    cur.execute("SELECT * FROM USER")
    query_details = cur.fetchall()
    
    for det in query_details:
        if det[1] == email:
            return make_response({'message': "User exists already"}, 400)
        
    sha256_password = hashlib.sha256(password.encode())
    encrypted_password = sha256_password.hexdigest()

    #store encrypted password in aws secrets manager (email: encrypted pw)
    #reference: https://www.youtube.com/watch?v=1WH3cocoWIY
 
    secret_payload = {
        "email": email,
        "password": encrypted_password
    }

    aws_secrets_client.create_secret(Name=email, SecretString=json.dumps(secret_payload))

    data = (rand_id, email, firstName, lastName, encrypted_password, accountType, False, "None")
    cur.execute(insert_stmt, data)

    db_conn.commit()
    #db_conn.close()
    return make_response({'message': "Success"}, 200)


#this route handles adding a new listing to the database in addition to adding it's corresponding image to an S3 bucket. 
#The image names will be equivalent to each listing's id to make it easier for querying later
#Reference: https://www.youtube.com/watch?v=EvHltGpbSqo
@application.route("/add-listing", methods=["POST"])
def addListing():

    cur = db_conn.cursor()
    data = request.get_json()

    
    use_stmt = ("USE scotiaRentalDB")


    insert_stmt = (
    "INSERT INTO LISTINGS (ListingId, Name, Description, Amenities, Price, Location) "
    "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    #setting up data to be inserted into DB
    #reference -> https://stackoverflow.com/questions/72926478/how-do-you-auto-generate-a-random-id-for-an-sqlite-database-table
    listing_id = random.randint(10000000, 99999999) #generates random 8 digit number
    if listing_id in unique_user_ids:
        listing_id = random.randint(10000000, 99999999)
    
    listing_name = data['name']
    listing_description = data['description']
    listing_amenities = data['amenities']
    listing_price = data['price']
    listing_location = data['location']

    new_listing_data = (listing_id, listing_name, listing_description, listing_amenities, listing_price, listing_location)


    try:
        cur.execute(use_stmt)
        cur.execute(insert_stmt, new_listing_data)
        db_conn.commit()
        return make_response({'message': "Success adding new listing", 'listing':new_listing_data}, 200)
    except:
        return make_response({'message': "Failed to add new listing"}, 500)
    


#two-step process, get the listing data from the data base, then also retrive the image url from S3 bucket.
@application.route("/get-listings", methods=["GET"])
def getListings():
    use_stmt = ("USE scotiaRentalDB")
    get_stmt = ("SELECT * FROM LISTINGS")
    cur = db_conn.cursor()

    bucket_name = 'scotia-rentals-listings-bucket'
    bucket_objects = s3.list_objects_v2(Bucket=bucket_name)
    try:
        cur.execute(use_stmt)
        cur.execute(get_stmt)
        listing_data = cur.fetchall()
        #print(listing_data)
        
        #if we have things(content) in our bucket object append their url's to the image_urls array 
        if 'Contents' in bucket_objects:      
            return make_response({'message': "Success getting listings", 'listings':listing_data, 'image_sources': bucket_objects['Contents']}, 200)
        else:
            print("Failed to fetch S3 bucket objects")
            return make_response({'message': "Failed to fetch S3 bucket objects"}, 500)
                
    except:
        print("Failed to get listings")
        return make_response({'message': "Failed to get listings"}, 500)
    

@application.route("/delete-listing", methods=["DELETE"])
def deleteListing():
    data = request.get_json()
    listing_id = data['listing_id']
    delete_stmt = "DELETE FROM LISTINGS WHERE ListingId = %s"
    
    try:
        with db_conn.cursor() as cur:
            cur.execute("USE scotiaRentalDB")  
            cur.execute(delete_stmt, (listing_id,))
        db_conn.commit()
        return make_response({'message': "Success deleting listing", 'listing_id': listing_id}, 200)
    except Exception as e:
        logging.error("Failed to delete listing: %s", e)
        db_conn.rollback()
        return make_response({'message': "Failed to delete listing"}, 500)

@application.route("/add-listing-to-favorites", methods=["POST"])
def addListingToFavorites():

    cur = db_conn.cursor()
    data = request.get_json()
  
    use_stmt = ("USE scotiaRentalDB")

    insert_stmt = (
    "INSERT INTO FAVORITES (ListingId, Name, Description)"
    "VALUES (%s, %s, %s)"
    )
    
    listing_id = data['listing_id']
    listing_name = data['listing_title']
    listing_description = data['listing_description']   


    new_listing_data = (listing_id, listing_name, listing_description)

    try:
        cur.execute(use_stmt)
        cur.execute(insert_stmt, new_listing_data)
        db_conn.commit()
        return make_response({'message': "Success adding listing to favorite", 'listing':new_listing_data}, 200)
    except Exception as e:
        logging.error("Failed to delete listing: %s", e)
        return make_response({'message': "Failed to add new listing to favorite"}, 500)


@application.route("/delete-listing-from-favorites", methods=["DELETE"])
def deleteListingFromFavorites():
    data = request.get_json()
    listing_id = data['listing_id']
    delete_stmt = "DELETE FROM FAVORITES WHERE ListingId = %s"
    
    try:
        with db_conn.cursor() as cur:
            cur.execute("USE scotiaRentalDB")  
            cur.execute(delete_stmt, (listing_id,))
        db_conn.commit()
        return make_response({'message': "Success deleting listing from favorites", 'listing_id': listing_id}, 200)
    except Exception as e:
        logging.error("Failed to delete listing: %s", e)
        db_conn.rollback()
        return make_response({'message': "Failed to delete listing"}, 500)


@application.route("/get-favorites-listings", methods=["GET"])
def getFavoritesListings():
    use_stmt = ("USE scotiaRentalDB")
    get_stmt = ("SELECT * FROM FAVORITES")
    cur = db_conn.cursor()

    bucket_name = 'scotia-rentals-listings-bucket'
    bucket_objects = s3.list_objects_v2(Bucket=bucket_name)

    try:
        cur.execute(use_stmt)
        cur.execute(get_stmt)
        listing_data = cur.fetchall()

        if 'Contents' in bucket_objects:        
            return make_response({'message': "Success getting listings", 'listings':listing_data, 'image_sources': bucket_objects['Contents']}, 200)
                
    except:
        return make_response({'message': "Failed to get listings"}, 500)


#this route handles processing payments via SQUARE
@application.route("/process-payment", methods=['POST'])
def processPayment():
    
    if request.content_type != 'application/json':
        print(request.content_type)
        return make_response({'message': 'Unsupported Media Type'},  415)
    
    create_payment_payload = {
        "source_id": request.json['nonce'],

        #in production would need to modify this to get realtime data from the front-end
        "amount_money": {
            "amount": 1000000,
            "currency": "USD"
        },
        "idempotency_key": request.json['idempotency_key']
    }

    #in the future can create a custom method to list payments as per user's unique nonce. this is just a POC.
    list_payments_payload = {
        "sort_order": 'DESC',
        "location_id": 'L5S30KEFRY41W',
        "last_4": '0009',
        "card_brand": 'AMEX',
        "limit": 10,
    }

    create_payment = square_client.payments.create_payment(create_payment_payload)
    list_payments = square_client.payments.list_payments(list_payments_payload)
    
    
    if create_payment.is_success():
        print(list_payments)
        return make_response({'message': "Success Creating Payment", "create_payment_json_body": json.dumps(create_payment.body), "list_payments_json_body": json.dumps(list_payments.body),}, 200)
    elif create_payment.is_error():
        return make_response({'message': "Error Creating Payment", "JSON_BODY": json.dumps(create_payment.errors)}, 400)

    


if __name__ == "__main__":
    application.run(port='8080', debug=True)


#references -> https://www.youtube.com/watch?v=7LNl2JlZKHA
