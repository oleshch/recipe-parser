import json
from PIL import Image
import pytesseract

# Replace with the path to your image
image_path = './recipe.png'

# Read the image with OCR
text = pytesseract.image_to_string(Image.open(image_path))

with open('recipe.txt', 'w') as outfile:
    outfile.write(text)

# Parse the text and convert it into schema.org/Recipe format
recipe = {
    '@context': 'http://schema.org/',
    '@type': 'Recipe',
    'name': '',
    'ingredients': [],
    'instructions': ''
}

# Parse the recipe name
lines = text.split('\n')
recipe['name'] = lines[0]

# Parse the ingredients
ingredients = []
for line in lines[1:]:
    if line.strip() == '':
        # End of ingredients list, break the loop
        break
    ingredients.append(line)
recipe['ingredients'] = ingredients

# Parse the instructions
instructions = []
in_instructions = False
for line in lines:
    if in_instructions:
        instructions.append(line)
    if line.strip().lower() == 'instructions':
        in_instructions = True
recipe['instructions'] = '\n'.join(instructions)

# Save the recipe as JSON
with open('recipe.json', 'w') as outfile:
    json.dump(recipe, outfile, indent=2)
