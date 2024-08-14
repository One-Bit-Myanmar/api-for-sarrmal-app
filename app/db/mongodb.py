from app.core.config import connect_to_database


# this is like a database dependency
# this get the specific database from one cluster
# I pull up the food_recommendation_database
# if database not exist, it will create automatically
def get_db():
    db = connect_to_database()["food_recommendation_database"]
    try:
        yield db # provide database connection
    finally:
        pass
        