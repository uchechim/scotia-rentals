#add_listing_test
from flask_app.services.db_services import connect_to_aws_db
from flask import json

def test_add_listing(test_server):

    test_listing_data = {
        'name' : 'test_listing_name',
        'description' :'test_listing',
        'amenities' : 'lorem_ipsum_test',
        'price' : 5,
        'location':'test_location'
    }

    response = test_server.post('/add-listing', data=json.dumps(test_listing_data), content_type='application/json')

    assert response.status_code == 200
    assert response.json['message'] == 'Success adding new listing'
    assert response.json['listing'][-1] == 'test_location'

    db_connection = connect_to_aws_db()
    cursor = db_connection.cursor()

    cursor.execute("DELETE FROM LISTINGS WHERE Location = %s", (test_listing_data['location'],))
    db_connection.commit()
    db_connection.close()



#get_listing_test
def test_get_listing(test_server):
    response = test_server.get("/get-listings")

    assert response.status_code == 200
    assert response.json['message'] == "Success getting listings"

   
#delete_listing_test
def test_delete_listing(test_server):

    test_listing_data = {
        'name' : 'test_listing_name',
        'description' :'test_listing',
        'amenities' : 'lorem_ipsum_test',
        'price' : 5,
        'location':'test_location'
    }

    add_response = test_server.post('/add-listing', 
                                    data=json.dumps(test_listing_data), 
                                    content_type='application/json')

    assert add_response.status_code == 200
    assert add_response.json['message'] == 'Success adding new listing'
    assert add_response.json['listing'][-1] == 'test_location'

    added_listing_unique_id = add_response.json['listing'][0]
    test_listing_data['listing_id'] = added_listing_unique_id

    delete_response = test_server.delete('/delete-listing', 
                                data=json.dumps(test_listing_data), 
                                content_type='application/json')
    
    assert delete_response.status_code == 200
    assert delete_response.json['message'] == 'Success deleting listing'
    assert delete_response.json['listing_id'] == added_listing_unique_id
