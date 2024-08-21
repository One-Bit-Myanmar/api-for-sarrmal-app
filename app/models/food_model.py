import re
import google.generativeai as genai
from PIL import Image
import json

#import gemini api key
#from app.core.config import GEMINI_KEY

#config the genai to use
#genai.configure(api_key=GEMINI_KEY)

# Gemini Pro Model
GEMINI_PRO = genai.GenerativeModel('gemini-pro')
# Gemini Pro 1.5 Model
GEMINI_PRO_1O5 = genai.GenerativeModel('gemini-1.5-pro')
# Regex pattern to match the text outside of the curly 
PATTERN = r'```json\s*({.*?})\s*```'


def get_calories_from_img(image: Image.Image):
    # generate the response 
    response = GEMINI_PRO_1O5.generate_content([
        """what is the total calorie count? Give by the following format
        {
            "name": str,
            "calories": int,
            "category": str,
            "ingredients": list[str],
            "url_to_how_to_cook": str,
            "image_url": str,
            "meal_time": str,
        }, 

        if user can't provide the food image then you have to response like this
        {
            "message": "{your message is in here}"
        }
        
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
    

# recommend food with Gemini AI and return json object of food
def generate_food_suggestion(user_info: str):
    try:
        model = genai.GenerativeModel(model_name='tunedModels/food-suggestion-ai-v1-uss801z982xp')
        print(genai.configure())
        result = model.generate_content(user_info)
        print(result.text)
        response = json.loads(result.text)
        return response
    
    except json.JSONDecoder as json_err:
        pass

    except Exception as e:
        pass

    return None

# print(generate_food_suggestion(
#     """{
#   "weight": 60,
#   "height": 165,
#   "age": 25,
#   "diseases": ["None"],
#   "allergies": ["Peanuts"],
#   "gender": "Female",
#   "exercise": "High"
# }"""
# ))