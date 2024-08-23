import re
from datetime import datetime


def is_valid_email(email: str) -> bool:
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, email) is not None


def calculate_age(birthdate: str) -> int:
    # Convert the birthdate string to a datetime object
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    
    # Get the current date
    today = datetime.today()
    
    # Calculate the age
    age = today.year - birthdate.year
    
    # Adjust age if the birthday hasn't occurred yet this year
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age -= 1
    
    return age