from flask import Blueprint, request, make_response
from flask_app.services.db_services import connect_to_aws_db
from flask_app.utils.helpers import generate_random_id
from flask_app.services.aws_services import list_s3_objects


listings_blueprint = Blueprint('listings', __name__)

#this route handles adding a new listing to the database in addition to adding it's corresponding image to an S3 bucket. 
#The image names will be equivalent to each listing's id to make it easier for querying later
#Reference: https://www.youtube.com/watch?v=EvHltGpbSqo
@listings_blueprint.route("/add-listing", methods=["POST"])
def addListing():
    data = request.get_json()

    db_connection = connect_to_aws_db()
    cursor = db_connection.cursor()

    #extract data from user request and generate a unique listing_id
    listing_name = data['name']
    listing_description = data['description']
    listing_amenities = data['amenities']
    listing_price = data['price']
    listing_location = data['location']

    while True:
        listing_id = generate_random_id()
        cursor.execute("SELECT ListingId FROM LISTINGS WHERE ListingId = %s", (listing_id,))

        if not cursor.fetchone():
            break


    #add the new listing's data to the database
    insert_stmt = (
    "INSERT INTO LISTINGS (ListingId, Name, Description, Amenities, Price, Location) "
    "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    new_listing_data = (listing_id, listing_name, listing_description, listing_amenities, listing_price, listing_location)

    
    try:
        cursor.execute("USE scotiaRentalDB")
        cursor.execute(insert_stmt, new_listing_data)
        db_connection.commit()
       
        return make_response({'message': "Success adding new listing", 'listing':new_listing_data}, 200)
    
    except:
        return make_response({'message': "Failed to add new listing"}, 500)
    
    finally:
        db_connection.close()
    


#two-step process, get the listing data from the data base, then also retrive the image url from S3 bucket.
@listings_blueprint.route("/get-listings", methods=["GET"])
def getListings():
    db_connection = connect_to_aws_db()
    try:
        s3_bucket_content = list_s3_objects() #list all the contents currently present in the s3 bucket

        #if bucket is empty or some type of failure occured whilst fetching contents, return failure response else, return listing data + img_urls
        if not s3_bucket_content:
            return make_response({'message': "Failed to fetch S3 bucket objects"}, 500)

        #connect to db and query all existing listings
        
        cursor = db_connection.cursor()

        cursor.execute("USE scotiaRentalDB")
        cursor.execute("SELECT * FROM LISTINGS")
        
        listing_data = cursor.fetchall()

        #if we have things(content) in our bucket object append their url's to the image_urls array 
        return make_response({'message': "Success getting listings", 'listings':listing_data, 'image_sources': s3_bucket_content}, 200)
    
    except:
        s3_bucket_content = list_s3_objects()
        db_connection.close()
        return make_response({'message': "Failed to get listings", 'image_sources': s3_bucket_content}, 500)
    finally:
        db_connection.close()
    

@listings_blueprint.route("/delete-listing", methods=["DELETE"])
def deleteListing():
    data = request.get_json()
    listing_id = data['listing_id']

    
    try:
        #connect to db and delete the listing that matches the ID passed via the frontend
        db_connection = connect_to_aws_db()

        delete_stmt = "DELETE FROM LISTINGS WHERE ListingId = %s"
        cursor = db_connection.cursor()
        
        cursor.execute("USE scotiaRentalDB")  
        cursor.execute(delete_stmt, (listing_id,))

        db_connection.commit()


        return make_response({'message': "Success deleting listing", 'listing_id': listing_id}, 200)
    
    except Exception as e:
     
        return make_response({'message': "Failed to delete listing", 'error message': e}, 500)
    finally:
        db_connection.close()