import requests
from app.core.config import UNSPLASH_ACCESS_KEY_1, UNSPLASH_ACCESS_KEY_2


#serach image for recommended food
def serach_for_food_image(food_name):
    UNSPLASH_ACCESS_KEY = UNSPLASH_ACCESS_KEY_2
    url = f"https://api.unsplash.com/search/photos?page=1&query={food_name} food&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"
    result = requests.get(url)
    
    if result.status_code != 200:
        UNSPLASH_ACCESS_KEY = UNSPLASH_ACCESS_KEY_1
        result = requests.get(url)
    
    if result.status_code == 200:
        data = result.json()
        if data['results']:
            return data['results'][0]['urls']['small']
        else:
            return {"error": "didnt find image"}
    return {"error": "something wrong with image searching server"}