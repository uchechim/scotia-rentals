from square.client import Client

def connect_to_square_client(access_token):
    return Client(access_token=access_token, environment='sandbox')