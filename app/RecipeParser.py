from pathlib import Path
import json
import pickle as pickle
from shutil import copy

def RecipeParser(p):
    RecipeName = {}
    RecipeCategory = {}
    PageName = {}
    JSONPath = {}
    ImagePath = {}

    p = Path(p)
    for i,val in enumerate(p.iterdir()):
        JSON = Path(val, 'recipe.json')
        JSONPath[i] = JSON # Path to recipe data for page loading
        with open(JSON, 'r') as file:
            data = json.load(file)
        SafeName = "".join(char for char in data["name"] if char.isalnum() or char == ' ')
        RecipeName[i] = SafeName # Save recipe name without any special characters
        PageName[SafeName.replace(' ','')] = i # Save above name without spaces for URLs
        
        if 'recipeCategory' in data:    
            RecipeCategory[i] = data['recipeCategory'] # Categories for filter buttons
        else:
            RecipeCategory[i] = 'Not Assigned'
        
        if Path(val, 'full.jpg').exists(): # image types: thumb.jpg, full.jpg, thumb16.jpg (icon)
            copy(Path(val, 'full.jpg'), Path(Path.cwd(),'static', 'fulls', f'{SafeName}.jpg'))
            copy(Path(val, 'thumb.jpg'), Path(Path.cwd(),'static', 'thumbs', f'{SafeName}.jpg'))
            ImagePath[i] = f'{SafeName}.jpg'
    del data
    del SafeName
    del JSON

    with open(Path(Path.cwd(), 'RecipeData.pkl'), 'wb') as f:
        pickle.dump([RecipeName,RecipeCategory, PageName, JSONPath, ImagePath], f)