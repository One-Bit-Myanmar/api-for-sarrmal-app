from app.core.config import connect_to_database


# this is like a database dependency
# this get the specific database from one cluster
# I pull up the food_recommendation_database
# if database not exist, it will create automatically
def get_db():
    client = connect_to_database() # connect the Mongodb Database
    db = client["food_recommendation_database"] # get the specific database
    try:
        print("DB connected successfully")
        yield db # provide database connection
    finally:
        client.close()  #ensure the connection is close 
        