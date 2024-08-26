import requests
from app.core.config import OAUTH_API, SEARCH_ENGINE_ID


#serach image for recommended food
# def serach_for_food_image(food_name):
#     UNSPLASH_ACCESS_KEY = UNSPLASH_ACCESS_KEY_2
#     url = f"https://api.unsplash.com/search/photos?page=1&query={food_name} food&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"
#     result = requests.get(url)
    
#     if result.status_code != 200:
#         UNSPLASH_ACCESS_KEY = UNSPLASH_ACCESS_KEY_1
#         result = requests.get(url)
    
#     if result.status_code == 200:
#         data = result.json()
#         if data['results']:
#             return data['results'][0]['urls']['small']
#         else:
#             return {"error": "didnt find image"}
#     return {"error": "something wrong with image searching server"}

def serach_for_food_image(search_query):
    """
    Searches for an image using Google Custom Search API and returns the link to the first image result.

    Parameters:
    search_query (str): The search query string.

    Returns:
    str: The link to the first image result or a message if no results are found.
    """
    API_KEY = OAUTH_API
    SEARCH_ENGINE_ID = SEARCH_ENGINE_ID

    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'searchType': 'image'
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        if 'items' in result:
            return result['items'][0]['link']
        else:
            return {"error": "didnt find image"}
    else:
        return {"error": "something wrong with image searching server"}