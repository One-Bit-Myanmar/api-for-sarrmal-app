## Food Recommendation API

**NOTE: please don't change everything in main branch, if you want to change you have to create new branch with your desired name.**

> You can also check how the main branch is developed by checking the other branches, the branches are as follow....
- sample-api: testing fastapi, just pure
- api-with-mongodb: testing with mongodb database


1. Clone the repo

```git
git clone https://github.com/Hein-HtetSan/api-for-sarrmal-app.git
```

Copy the .env.example as .env
```git
cp .env.example .env
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

```mermaid
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