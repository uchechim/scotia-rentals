
from flask import Blueprint, request, make_response, json
from flask_app.services.square_payment_services import connect_to_square_client
from config import Config


payments_blueprint = Blueprint('payment', __name__)


#this route handles processing payments via SQUARE
@payments_blueprint.route("/process-payment", methods=['POST'])
def processPayment():
    
    if request.content_type != 'application/json':
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

    try:

        square_client = connect_to_square_client(Config.SQUARE_ACCESS_TOKEN)
        create_payment = square_client.payments.create_payment(create_payment_payload)
        list_payments = square_client.payments.list_payments(list_payments_payload)
    
    
        if create_payment.is_success():
            return make_response({'message': "Success Creating Payment", "create_payment_json_body": json.dumps(create_payment.body), "list_payments_json_body": json.dumps(list_payments.body),}, 200)
    except:
        return make_response({'message': "Error Creating Payment", "JSON_BODY": json.dumps(create_payment.errors)}, 400)
    finally:
        print("end of payment process")

