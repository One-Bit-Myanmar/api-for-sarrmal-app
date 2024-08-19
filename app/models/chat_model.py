from app.core.config import GEMINI_KEY 
import google.generativeai as genai

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
    # init the model
    model = genai.GenerativeModel(
        "gemini-pro", 
        generation_config=generation_config
    )
    chat_session = genai.ChatSession(model=model)  # Initialize chat session
    gemini_response = chat_session.send_message(prompt)
   # Access text using the correct attribute (replace 'content.parts[0].text' if needed)
    generated_text = gemini_response.candidates[0].content.parts[0].text  
    # return the generated text
    return generated_text