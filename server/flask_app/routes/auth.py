from flask import Blueprint, request, make_response
from flask_app.services.aws_services import get_user_auth_secret, create_user_auth_secret
from flask_app.services.db_services import connect_to_aws_db
from flask_app.utils.helpers import hash_password, generate_random_id

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route("/signin", methods=['POST'])
def signin():

    #get data from request
    data = request.get_json()
    email = data['email']
    password = data['password']

    #hash user password in order to compare to password stored in AWS secrets manager
    encrypted_user_password = hash_password(password)
    aws_user_secret_payload = get_user_auth_secret(email)

    #check if passwords match or not, if they dont, return 400
    if not aws_user_secret_payload or aws_user_secret_payload['password'] != encrypted_user_password:
         return make_response({'message': "Invalid Credentials"}, 400)

    #if passwords match, sign in user and return user data to front-end , return 200
    db_connection = connect_to_aws_db()
    cursor = db_connection.cursor()

    cursor.execute("USE scotiaRentalDB")
    cursor.execute("SELECT * FROM USER WHERE email = %s AND password = %s", (email, encrypted_user_password))

    user_details = cursor.fetchone()

    #close db_connection after query is performed
    db_connection.close()
    
    #return user data to front-end    
    if user_details:
        
        user = {
            'id':user_details[0], 
            'firstName':user_details[1],
            'lastName':user_details[2],
            'email':user_details[3],
            'password':user_details[4],
            'accountType':user_details[5],
            'isAuthenticated':user_details[6],
            'userToken':user_details[7]
            }
        
        return make_response({'message': "Successfully Signed In", 'user': user}, 200)
    else:
        return make_response({'message': "Invalid Credentials"}, 400)

    
@auth_blueprint.route("/signup", methods=['POST'])
def signup():

    #get user data from front end

    data = request.get_json()
    email = data['email']
    firstName = data['firstName']
    lastName = data['lastName']
    password = data['password']
    accountType = data['accountType']

    #validate email -> implement later using REGEX?

    #encrypt user password
    encrypted_password = hash_password(password)

    #query the DB to see if user already exists, if user DNE, add user to DB
    db_connection = connect_to_aws_db() 
    cursor = db_connection.cursor()

    cursor.execute("USE scotiaRentalDB")
    cursor.execute("SELECT * FROM USER WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return make_response({'message': "User exists already"}, 400)
    else:
        #generate random id for user and validate it's existence
        while True:
            user_id = generate_random_id()
            cursor.execute("SELECT UserId FROM USER WHERE UserId = %s", (user_id,))

            #if query doesn't return a record then this is a unique id
            if not cursor.fetchone():
                break

        #add user to database
        insert_stmt = ("INSERT INTO USER (UserId, Email, FirstName, LastName, Password, AccountType, IsAuthenticated, Token) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                       )
        data = (user_id, email, firstName, lastName, encrypted_password, accountType, False, "None")
        cursor.execute(insert_stmt, data)
        db_connection.commit()
        db_connection.close()

        #add secret to secret manager
        create_user_auth_secret(user_email=email, encrypted_password=encrypted_password)

        return make_response({'message': "Successfully signed up user {user_email}".format(user_email=email)}, 200)
