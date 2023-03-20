import os
import re
import sys
import json
import requests
import nextcloud_client
from bs4 import BeautifulSoup


# Local Files
script_path = os.path.dirname(os.path.realpath(__file__))

# Load Creds File
with open(script_path + '/urls.json') as file:
  urls = json.load(file)

def create_receipe_json(url, recipeCategory):
    # Send a GET request to the URL and store the response
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # schema.org/Recipe format
    recipe = {
        '@context': 'http://schema.org',
        '@type': 'Recipe',
        'name': '',
        'image': '',
        'description': '',
        'recipeIngredient': [],
        'recipeInstructions': '',
        'recipeCategory': '',
        'url': ''
    }

    # Get the recipe title
    title = soup.find('div', class_='recipe_name').get_text()
    recipe['name'] = title

    recipe['recipeCategory'] = recipeCategory

    # Make the Folder
    save_path = os.path.join(script_path + '/output', title)
    os.makedirs(save_path, exist_ok = True)

    # Get the recipe ingredients
    all_ingredients = soup.find('div', class_='ingredients').get_text().split('\n')

    ingredients = []
    for li in all_ingredients:
        if len(li) > 3:
            ingredient = li.strip()
            ingredients.append(ingredient)
    recipe['recipeIngredient'] = ingredients


    # Get the recipe instructions
    directions = soup.find('div', class_='directions').get_text().split('\n')

    instructions = []
    for p in directions:
        if len(p) > 3:
            instruction = re.sub('(^\d*\. )', '', p)
            instruction = re.sub('(^\d* )', '', instruction)
            instructions.append(instruction)
    recipe['recipeInstructions'] = instructions

    try:
        soup.find('div', class_='recipe_overview').get_text()
    except:
        description = ''
    else:
        description = soup.find('div', class_='recipe_overview').get_text()
    recipe['description'] = description.replace('\n','')

    image = soup.find('div', class_='recipe_img').img['src']
    recipe['image'] = image

    # Download Image
    img_data = requests.get(image).content
    with open(save_path + '/full.jpg', 'wb') as handler:
        handler.write(img_data)


    recipe['url'] = url


    # Save the recipe data to a JSON file
    with open(save_path + '/recipe.json', 'w') as f:
        json.dump(recipe, f, indent=3)

def upload_files():
    nc = nextcloud_client.Client('https://nextcloud.lesh.ca')
    nc.login('oleshch', 'go%23I0Pn%24DUd3%5Ej%23%21POq7E0xCH')
    nc.mkdir('testdir')


def main():
    for recipe in urls['recipes']:
        url = recipe['url']
        recipeCategory = recipe['recipeCategory']
        print("Working on: ", url)
        create_receipe_json(url, recipeCategory)


if __name__ == "__main__":
    main()