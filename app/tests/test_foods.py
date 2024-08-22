import subprocess

ai_input = {
  "weight": 60,
  "height": 165,
  "age": 25,
  "diseases": ["None"],
  "allergies": ["Peanuts"],
  "gender": "Female",
  "exercise": "High"
}


result = subprocess.run(
            f"python D:\\Code\\git\\api-for-sarrmal-app\\app\\services\\injection_script.py '{str(ai_input)}'",
              shell=True, capture_output=True, text=True)


print(result)
print(type(result))