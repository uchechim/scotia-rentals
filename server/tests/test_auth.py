from flask import json
from flask_app.services.db_services import connect_to_aws_db
from flask_app.utils.helpers import hash_password


def test_signup(test_server):

    #Define test user to sign up
    test_user_data = {
        'email': 'testuser11312@example.com',
        'firstName': 'Test',
        'lastName': 'User',
        'password': 'password',
        'accountType': 'Landlord',
    }

    #mock an api call (signup) to the server using the test user data
    response = test_server.post('/signup', data=json.dumps(test_user_data), content_type='application/json')
    
    #verify that sign up was successfull
    assert response.status_code == 200
    assert response.json['message'] == 'Successfully signed up user testuser11312@example.com'


    #verify that user exists in the database
    db_connection = connect_to_aws_db()
    cursor = db_connection.cursor()

    cursor.execute("USE scotiaRentalDB")
    cursor.execute("SELECT * FROM USER WHERE Email = %s", (test_user_data['email'],))
    db_test_user = cursor.fetchone()

    assert db_test_user is not None
    assert db_test_user[1] == test_user_data['email']
    assert db_test_user[2] == test_user_data['firstName']
    assert db_test_user[3] == test_user_data['lastName']
    assert db_test_user[4] == hash_password(test_user_data['password'])
    assert db_test_user[5] == test_user_data['accountType']

    #delete user from database to allow for future tests using the same credentials.
    cursor.execute("DELETE FROM USER WHERE email = %s", (test_user_data['email'],))
    db_connection.commit()
    db_connection.close()

'''
def test_signin(test_client):
    #Define test user to sign in
    pass'''