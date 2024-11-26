from flask import Flask, request, render_template
import requests
import json
import os

# Set your API key here
API_KEY = 'AIzaSyDAmz79p9wnxtFL03OoFjVf37S_NLKgP5Y'  # Make sure to set your API key in the environment variables

app = Flask(__name__)

# Function to generate a recipe based on user input
def generate_recipe(ingredients, meal_type, dietary_restrictions):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    headers = {
        "Content-Type": "application/json",
    }

    # Create the prompt for the model
    prompt = f"I have: {', '.join(ingredients)}. I'm looking for a {meal_type} recipe."
    if dietary_restrictions:
        prompt += f" Dietary restrictions: {dietary_restrictions}."

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Send the POST request to the API
    response = requests.post(url, headers=headers, params={"key": API_KEY}, data=json.dumps(data))
   

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        if 'candidates' in response_data and len(response_data['candidates']) > 0:
            recipe = response_data['candidates'][0]['content']['parts'][0]['text']
            return recipe
        else:
            return "Error: Unexpected response structure. No 'candidates' found."
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route('/', methods=['GET', 'POST'])
def index():
    recipe = ""
    if request.method == 'POST':
        ingredients = request.form.get('ingredients').split(',')
        ingredients = [ingredient.strip().lower() for ingredient in ingredients]
        meal_type = request.form.get('meal_type')
        dietary_restrictions = request.form.get('dietary_restrictions')

        # Generate the recipe
        recipe = generate_recipe(ingredients, meal_type, dietary_restrictions)

    return render_template('index.html', recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)
