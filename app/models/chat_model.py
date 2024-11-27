from app.core.config import GEMINI_KEY 
import google.generativeai as genai
from google.api_core import exceptions
from fastapi import HTTPException
import re

# Configuration
genai.configure(api_key=GEMINI_KEY)
generation_config = {
    "temperature": 0.25,
    "max_output_tokens": 1024,
    "top_k": 40,
    "top_p": 0.95
}

# Function to generate a response using Google Generative AI
def generate_response(prompt):
    try:
        # Define a system message to instruct the AI
        system_message = (
            "You are an AI specialized in food-related topics. You can only answer questions about food, "
            "nutrition, calories, healthy eating, recipes, and other food-related matters. "
            "If the question is unrelated to food, politely inform the user."
        )
        # Combine the system message with the user's prompt
        final_prompt = f"{system_message}\n\nUser: {prompt}"
        # init the model
        model = genai.GenerativeModel(
            "gemini-pro", 
            generation_config=generation_config
        )
        chat_session = genai.ChatSession(model=model)  # Initialize chat session
        gemini_response = chat_session.send_message(final_prompt)
        # Access text using the correct attribute (replace 'content.parts[0].text' if needed)
        generated_text = gemini_response.candidates[0].content.parts[0].text  
        # return the generated text
        return generated_text
    except exceptions.FailedPrecondition as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {e}")