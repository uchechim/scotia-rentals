#add_listing
from flask_app.services.db_services import connect_to_aws_db
from flask import json

def test_add_favorite_listing(test_server):

    test_favorites_listing_data = {
        'listing_id' : 99112191029192019210291020190201,
        'listing_title' :'test_listing',
        'listing_description' : 'lorem_ipsum_test'
    }

    response = test_server.post('/add-listing-to-favorites', data=json.dumps(test_favorites_listing_data), content_type='application/json')

    assert response.status_code == 200
    assert response.json['message'] == 'Success adding listing to favorite'

    assert int(response.json['listing'][0]) == 99112191029192019210291020190201

    db_connection = connect_to_aws_db()
    cursor = db_connection.cursor()

    cursor.execute("DELETE FROM FAVORITES WHERE ListingId = %s", (test_favorites_listing_data['listing_id'],))
    db_connection.commit()
    db_connection.close()



#get_listing
def test_get_favorite_listing(test_server):
    response = test_server.get("/get-favorites-listings")

    assert response.status_code == 200
    assert response.json['message'] == "Success getting listings"
    
#delete_listing
def test_delete_favorite_listing(test_server):
    test_favorites_listing_data = {
        'listing_id' : 99112191029192019210291020190201,
        'listing_title' :'test_listing',
        'listing_description' : 'lorem_ipsum_test'
    }

    add_response = test_server.post('/add-listing-to-favorites', 
                                    data=json.dumps(test_favorites_listing_data), 
                                    content_type='application/json')

    assert add_response.status_code == 200
    assert add_response.json['message'] == 'Success adding listing to favorite'
    assert int(add_response.json['listing'][0]) == 99112191029192019210291020190201

    delete_response = test_server.delete('/delete-listing-from-favorites', 
                                data=json.dumps(test_favorites_listing_data), 
                                content_type='application/json')
    
    assert delete_response.status_code == 200
    assert delete_response.json['message'] == 'Success deleting listing from favorites'
    assert delete_response.json['listing_id'] == 99112191029192019210291020190201
 