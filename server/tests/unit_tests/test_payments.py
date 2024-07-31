'''from flask import json

need to install square SDK for python and generate a test nonce/token from the backend.


from flask_app.services.db_services import connect_to_aws_db
from flask_app.utils.helpers import hash_password

def test_process_payment(test_server):
    
    test_credit_card_details = {
        'nonce': 1038231904,
        'idempotency_key': 9048719981
    }

    response = test_server.post("/process-payment", 
                     data=json.dumps(test_credit_card_details), 
                     content_type='application/json')
    
    assert response.status_code == 200
    assert response.json['create_payment_json_body'] is not None
    assert response.json['list_payments_json_body'] is not None
'''