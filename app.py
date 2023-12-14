from flask import Flask, render_template, request
import requests
import json
import keys
app = Flask(__name__)

api_id = keys.id
api_key = keys.key
url = 'https://api.edamam.com/search'

@app.route('/') #homepage
def index():
    return render_template('index.html') #returning index file as homepage

@app.route('/results', methods=['POST']) #results page
def search():

    query = request.form['query']
    meal_type = request.form.get('mealType')
    preferences = request.form.getlist('preferences[]')
    minimum_Calories = request.form.get('minCal', type=int)
    maximum_Calories = request.form.get('maxCal', type=int)

    params = {
        'app_id': api_id,
        'app_key': api_key,
        'q': query,
        'mealType': meal_type,
        'dietAndHealth': preferences,
        'calories': f'{minimum_Calories}-{maximum_Calories}'
    }

    response = requests.get(url, params=params) #retrieving parameters
    data = json.loads(response.text)

    recipes = [] #empty list before retrieving recipes
    for hit in data.get('hits'): #'hits' where all the recipes are
        recipe = hit.get('recipe') #'recipe' where all the recipe information is
        recipes.append({ #adding recipes to list
            'label': recipe.get('label'), #name of recipe
            'url': recipe.get('url'), #url to recipe
            'image': recipe.get('image'), #image of recipe
            'ingredients': recipe.get('ingredientLines'), #ingredients of recipe
            'calories': round(recipe.get('calories', 'not specified')) #calories of recipe
        })

    return render_template('results.html', recipes=recipes, minimum_Calories=minimum_Calories, maximum_Calories=maximum_Calories)
    #returning recipes, minimum calories, and maximum calories to results page







