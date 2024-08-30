import re
import google.generativeai as genai
from PIL import Image
import json
import ast
from app.services.refresh_google_oauth import load_creds

#import gemini api key
#from app.core.config import GEMINI_KEY

#config the genai to use
creds = load_creds()
genai.configure(credentials=creds, transport="grpc")

# Gemini Pro Model
GEMINI_PRO = genai.GenerativeModel('gemini-pro')
# # Gemini Pro 1.5 Model
GEMINI_PRO_1O5 = genai.GenerativeModel('gemini-1.5-pro')
# Regex pattern to match the text outside of the curly 
PATTERN = r'```json\s*({.*?})\s*```'

# the func will handle to get calories from image
def get_calories_from_img(image: Image.Image):
    # generate the response 
    response = GEMINI_PRO_1O5.generate_content([
        """give me result by following format
        - meal time must be time format like this "00:00 AM"
        
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
    print(content_text)
    # Clean the response by removing the JSON-like structure
    match = re.search(PATTERN, content_text, re.DOTALL)
    if match:
        # Extract the JSON string
        json_string = match.group(1)
        # Convert the string to a Python dictionary
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
        model = genai.GenerativeModel(model_name=f'tunedModels/food-suggestion-ai-v3-t2z0eh7qpaq8')
        result = model.generate_content(user_info)
        print(result.text)
        result = _format_json_from_gemini(result.text)
        
        response = json.loads(result)
        return response
    
    except json.JSONDecodeError as json_err:
        print(json_err)
        try:
            response = ast.literal_eval(result)
            return response
        except Exception:
            print("error on ast.literal_eval")
            pass

    except Exception as e:
        pass

    return None


# get
def _format_json_from_gemini(text: str):
    front, end = 0, len(text) - 1

    while text[front] != '{':
        front += 1
    
    while text[end] != '}':
        end -= 1

    return text[front:end+1]

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