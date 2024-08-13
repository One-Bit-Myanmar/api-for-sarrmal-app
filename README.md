## Food Recommendation API

**NOTE: please don't change everything in main branch, if you want to change you have to create new branch with your desired name.**

> You can also check how the main branch is developed by checking the other branches, the branches are as follow....
- sample-api: testing fastapi, just pure
- api-with-mongodb: testing with mongodb database


1. Clone the repo

```git
git clone https://github.com/Hein-HtetSan/api-for-sarrmal-app.git
```

Create **env dir** and **credentials.env**
```shell
mkdir env
cd env
touch credentials.env
```

2. Create a Virtual Environment

```shell
python -m venv venv
```

3. Activate the Virtual Environment

```shell
# for windows
venv\Scripts\activate

# for mac
source venv/bin/activate
```

4. Install Dependencies

```shell
pip install -r requirements.txt
```

5. After installing new packages, don't forget to update (optional)

```shell
pip freeze > requirements.txt
```

6. Project Structures

```
your_app/
├── venv/                     # Virtual environment directory
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── recommendations.py
│   │   │   ├── users.py
│   │   │   ├── foods.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── mongodb.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── food.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── recommendation_model.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── food.py
│   │   ├── recommendation.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── recommendation_service.py
│   │   ├── user_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── common.py
│   └── tests/
│       ├── __init__.py
│       ├── test_recommendations.py
│       ├── test_users.py
│       ├── test_foods.py
├── data/
│   ├── raw/
│   ├── processed/
│   ├── trained_model/
│   │   ├── model.joblib
├── notebooks/
│   ├── data_preprocessing.ipynb
│   ├── model_training.ipynb
├── requirements.txt
├── .env
└── README.md
 ```

### Libs included

- fastapi: The main framework for building your API.
- uvicorn: ASGI server to run your FastAPI application.
- pydantic: For data validation and settings management.
- motor: Asynchronous MongoDB driver.
- pandas: Data manipulation and analysis library.
- scikit-learn: For machine learning algorithms and model handling.
- joblib: For model serialization and deserialization.
- python-dotenv: To load environment variables from a .env file.
- pytest: Framework for writing and running tests.
- httpx: For making HTTP requests in your tests.
- flake8: For checking the style and quality of your code.
- black: Code formatter.

### Project Structure Breakdown

> your_app/:

The root directory of your FastAPI project.

> venv/:

Virtual environment directory containing all the dependencies and packages installed for this project.

> app/:

Main application directory containing the core components of your FastAPI project.

> __init__.py:

Marks the app directory as a Python package.
main.py:

The entry point of the FastAPI application where the app is initialized and routes are included.

> api/:

Contains the API-related modules and routing.

> __init__.py:

Marks the api directory as a Python package.

> endpoints/:

Contains individual API endpoints or routes for different functionalities.

> __init__.py:

Marks the endpoints directory as a Python package.
recommendations.py:

API endpoints related to generating and managing food recommendations.
users.py:

API endpoints related to user management, such as registration, login, and profile updates.
foods.py:

API endpoints related to managing food items in the database.

> core/:

Core functionalities and configurations of the application.

> __init__.py:

Marks the core directory as a Python package.
config.py:

Application configuration settings, including environment variables and database connections.
security.py:

Security-related functions, such as password hashing, JWT token creation, and authentication.

> db/:

Database-related modules and models.

> __init__.py:

Marks the db directory as a Python package.
mongodb.py:

MongoDB connection and database handling logic.

> models/:

Contains database models that define the structure of data in MongoDB.

> __init__.py:

Marks the models directory as a Python package.
user.py:

Database model representing a user in the system.
food.py:

Database model representing a food item in the system.

> models/:

Contains machine learning models or any other business-related models.

> __init__.py:

Marks the models directory as a Python package.
recommendation_model.py:

Handles loading and using the machine learning model for food recommendations.

> schemas/:

Pydantic models (schemas) used for data validation and serialization.

> __init__.py:

Marks the schemas directory as a Python package.
user.py:

Schemas for user-related data validation (e.g., registration, login).
food.py:

Schemas for food-related data validation.
recommendation.py:

Schemas for recommendation-related data validation.

> services/:

Business logic and services that interact with the database and models.

> __init__.py:

Marks the services directory as a Python package.
recommendation_service.py:

Business logic for generating and managing food recommendations.
user_service.py:

Business logic for managing users.

> utils/:

Utility functions and common helpers used across the application.

> __init__.py:

Marks the utils directory as a Python package.
common.py:

Common utility functions used throughout the application.

> tests/:

Test cases for the application, ensuring all features work as expected.

> __init__.py:

Marks the tests directory as a Python package.
test_recommendations.py:

Test cases for the recommendation functionality.
test_users.py:

Test cases for user-related functionality.
test_foods.py:

Test cases for food-related functionality.

> data/:

Directory for storing datasets and trained models.

> raw/:

Raw, unprocessed data files.

> processed/:

Processed data files ready for use in model training.

> trained_model/:

Contains trained machine learning models, like model.joblib.

> notebooks/:

Jupyter notebooks for data analysis, preprocessing, and model training.

data_preprocessing.ipynb:

Notebook for data preprocessing.
model_training.ipynb:

Notebook for training the machine learning model.

> requirements.txt:

Lists all the Python packages required for the project.

> .env:

Environment variables, such as database connection strings and secret keys.

> README.md:

Project documentation providing an overview of the application, how to set it up, and how to use it.