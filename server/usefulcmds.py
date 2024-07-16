#Create/Delete/Update SQL Table queries
'''
CODE TO CREATE NEW TABLES IN SQL DB
cursor = db_conn.cursor()
use_stmt = ("USE scotiaRentalDB")
create_table = """CREATE TABLE USER(UserId int, Email varchar(255), FirstName varchar(255), LastName varchar(255), Password varchar(255), AccountType varchar(255), IsAuthenticated BOOLEAN, Token varchar(255));"""
cursor.execute(use_stmt)
cursor.execute(create_table)

#create TABLE LISTINGS
cursor = db_conn.cursor()
use_stmt = ("USE scotiaRentalDB")
create_table = """CREATE TABLE LISTINGS(ListingId int, Name varchar(255), Description varchar(255), Amenities varchar(255), Price DOUBLE, Location varchar(255));"""
cursor.execute(use_stmt)
cursor.execute(create_table)

#create TABLE FAVORITES
cursor = db_conn.cursor()
use_stmt = ("USE scotiaRentalDB")
create_table = """CREATE TABLE FAVORITES(ListingId int, Name varchar(255), Description varchar(255));"""
cursor.execute(use_stmt)
cursor.execute(create_table)
'''

'''
#CODE TO DELETE TABLES IN SQL DB

1 -
cursor = db_conn.cursor()
use_stmt = ("USE scotiaRentalDB")
cursor.execute(use_stmt)


2 - 
show_tables = """SHOW TABLES;"""
cursor.execute(show_tables)
tables = cursor.fetchall()
print(tables)


3 - 
delete_table = "DROP TABLE IF EXISTS LISTINGS;"
cursor.execute(delete_table)
tables = cursor.fetchall()
print(tables)


#CODE TO DELETE DATA IN SQL DB TABLE


1 - 
cursor = db_conn.cursor()
use_stmt = ("USE scotiaRentalDB")
cursor.execute(use_stmt)


2 -
show_tables = """SHOW TABLES;"""
cursor.execute(show_tables)
tables = cursor.fetchall()
print(tables)


3 -
clear_table = "DELETE FROM USER;"
cursor.execute(clear_table)
db_conn.commit()


4 -
clear_table = "DELETE FROM LISTINGS;"
cursor.execute(clear_table)
db_conn.commit()


5 -
clear_table = "DELETE FROM FAVORITES;"
cursor.execute(clear_table)
db_conn.commit()


6 - 
query = "SELECT * FROM USER;"
cursor.execute(query)
res = cursor.fetchall()
print(res)


#Get temporary AWS credentials.
client = boto3.client('sts', aws_access_key_id=aws_access_key_id_val, aws_secret_access_key=aws_secret_access_key_val)
response = client.get_session_token(DurationSeconds=3600)
print('AccessKeyId:', response['Credentials']['AccessKeyId'])
print('SecretAccessKey:', response['Credentials']['SecretAccessKey'])
print('SessionToken:', response['Credentials']['SessionToken'])
'''