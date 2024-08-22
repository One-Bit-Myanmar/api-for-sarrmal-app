# my_script.py
import sys
import google.generativeai as genai
import json
#from app.models.food_model import generate_food_suggestion

def generate_food_suggestion(user_info: str):
    try:
        model = genai.GenerativeModel(model_name='tunedModels/food-suggestion-ai-v1-uss801z982xp')
        result = model.generate_content(user_info)
        print(result.text)
        response = json.loads(result.text)
        return response
    
    except json.JSONDecoder as json_err:
        pass

    except Exception as e:
        pass

    return None


if __name__ == "__main__":
    # Get the input from the command line arguments
    if len(sys.argv) > 1:
        user_info = sys.argv[1]
        print(generate_food_suggestion(user_info))
    else:
        print("Please provide a name as a command-line argument.")
