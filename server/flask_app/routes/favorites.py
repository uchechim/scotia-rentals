#TODO -> add column to "favorites" called "favorites_user_id", Modify "get favorites", and "add listing to favorites", both functions should utilize the "favorites_user_id" for querying purposes
from flask import Blueprint, request, make_response
from flask_app.services.db_services import connect_to_aws_db
from flask_app.services.aws_services import list_s3_objects


favorites_blueprint = Blueprint('favorites', __name__)

@favorites_blueprint.route("/add-listing-to-favorites", methods=["POST"])
def addListingToFavorites():

    #connect to db and get favorite data from front end
    db_connection = connect_to_aws_db()
    cursor = db_connection.cursor()
    data = request.get_json()

    listing_id = data['listing_id']
    listing_name = data['listing_title']
    listing_description = data['listing_description']   
    
    
    new_listing_data = (listing_id, listing_name, listing_description)

    try:
        cursor.execute("USE scotiaRentalDB")

        insert_stmt = (
            "INSERT INTO FAVORITES (ListingId, Name, Description)"
            "VALUES (%s, %s, %s)"
        )

        cursor.execute(insert_stmt, new_listing_data)
        
        db_connection.commit()

        return make_response({'message': "Success adding listing to favorite", 'listing':new_listing_data}, 200)
    
    except Exception as e:
        return make_response({'message': "Failed to add new listing to favorite", 'Exception: ': e}, 500)
    
    finally:
        db_connection.close()

@favorites_blueprint.route("/delete-listing-from-favorites", methods=["DELETE"])
def deleteListingFromFavorites():
    db_connection = connect_to_aws_db()
    cursor = db_connection.cursor()

    data = request.get_json()
    listing_id = data['listing_id']
    
    
    try:     
        delete_stmt = "DELETE FROM FAVORITES WHERE ListingId = %s"
        cursor.execute("USE scotiaRentalDB")  
        cursor.execute(delete_stmt, (listing_id,))

        db_connection.commit()
  
        return make_response({'message': "Success deleting listing from favorites", 'listing_id': listing_id}, 200)
    
    except Exception as e:

        return make_response({'message': "Failed to delete listing", 'Exception: ': e}, 500)
    
    finally:
        db_connection.close()


@favorites_blueprint.route("/get-favorites-listings", methods=["GET"])
def getFavoritesListings():
    db_connection = connect_to_aws_db()
    cursor = db_connection.cursor()


    try:
        cursor.execute("USE scotiaRentalDB")
        cursor.execute("SELECT * FROM FAVORITES")
        listing_data = cursor.fetchall()

        s3_bucket_objects = list_s3_objects()
        if s3_bucket_objects:        
            return make_response({'message': "Success getting listings", 'listings':listing_data, 'image_sources': s3_bucket_objects}, 200)
                
    except:
        return make_response({'message': "Failed to get listings"}, 500)
    
    finally:
        db_connection.close()
