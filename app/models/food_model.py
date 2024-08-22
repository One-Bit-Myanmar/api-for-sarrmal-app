import re
import google.generativeai as genai
from PIL import Image
import json

# import gemini api key
from app.core.config import GEMINI_KEY

# config the genai to use
genai.configure(api_key=GEMINI_KEY)

# Gemini Pro Model
GEMINI_PRO = genai.GenerativeModel('gemini-pro')
# Gemini Pro 1.5 Model
GEMINI_PRO_1O5 = genai.GenerativeModel('gemini-1.5-pro')
# Regex pattern to match the text outside of the curly 
PATTERN = r'```json\s*({.*?})\s*```'


def get_calories_from_img(image: Image.Image):
    # generate the response 
    response = GEMINI_PRO_1O5.generate_content([
        """give me result by following format
        - meal time must be time format like this "12:00 AM"
        
        ```json{
            "name": str,
            "calories": int,
            "category": str,
            "ingredients": list[str],
            "how_to_cook": str,
            "meal_time": str,
        }```
        
        if the image is not food then return the following format
        ```json{
            "message": "short message"
        }```
        so that i can use in my fastapi 
        response route""",
        image])
    # content_text = response["content"]["parts"][0]["text"]
    content_text = response.text
    # Clean the response by removing the JSON-like structure
    match = re.search(PATTERN, content_text, re.DOTALL)
    if match:
        # Extract the JSON string
        json_string = match.group(1)
        # Convert the string to a Python dictionary
        print(json_string)
        try:
            # Convert the string to a proper Python dictionary
            json_dict = json.loads(json_string)
            return json_dict
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON: {str(e)}")
    else:
        raise ValueError("No JSON-like content found in the response.")
    

# clean the text file and return json file
def clean_and_convert_to_json(response_str):
    try:
        # Convert the string to a proper JSON object
        json_dict = json.loads(response_str)
        return json_dict
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON: {str(e)}")