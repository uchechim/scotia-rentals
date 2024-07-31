import pytest
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from config import Config
from flask_app import create_app

#fixture scope as module - This specifies that the fixture is set up once per module, and the same fixture is used across all tests in that module
@pytest.fixture(scope='module')
def test_server():
    

    #create an instance of the flask backend app and load config into it 
    test_flask_app = create_app()
    test_flask_app.config.from_object(Config) #(need to change this line later to use a testing configuration)

    #using the context of the test_flask_app (i.e - routes e.t.c) - Push the application context
    with test_flask_app.app_context():

        #create a test server for the Flask application, which can be used to simulate requests to the application without starting an actual server
        testing_client = test_flask_app.test_client()

        #allow the testing_client to be access globally 
        yield testing_client
