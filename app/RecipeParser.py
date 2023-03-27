from pathlib import Path
import json
import pickle as pickle
from shutil import copy

def RecipeParser(recipe_data_path):
    app.logger.info('Reading recipe data. . .')
    app.logger.info(recipe_data_path)  
    if not recipe_data_path.is_dir():
        app.logger.info('No recipe data found! Mount volume and restart container.')
        return
    img_full = Path(Path.cwd(), 'app', 'static', 'fulls')
    img_thumb = Path(Path.cwd(), 'app', 'static', 'thumbs')    
    if not img_full.exists():
        img_full.mkdir()
    if not img_thumb.exists():
        img_thumb.mkdir()
        
    RecipeName = {}
    RecipeCategory = {}
    PageName = {}
    JSONPath = {}
    ImagePath = {}

    for i,val in enumerate(recipe_data_path.iterdir()):
        JSONPath[i] = Path(val, 'recipe.json') # Path to recipe data for page loading
        
        with open(JSONPath[i], 'r') as file:
            data = json.load(file)
        # Save recipe name without any special characters, and without spaces for URLs
        RecipeName[i] = "".join(char for char in data["name"] if char.isalnum() or char == ' ') 
        PageName[RecipeName[i].replace(' ','')] = i
        
        if 'recipeCategory' in data:    
            RecipeCategory[i] = data['recipeCategory'] # Categories for filter buttons
        else:
            RecipeCategory[i] = 'Not Assigned'
        
        if Path(val, 'full.jpg').exists(): # image types: thumb.jpg, full.jpg, thumb16.jpg (icon)
            copy(Path(val, 'full.jpg'), Path(img_full, f'{RecipeName[i]}.jpg'))
            copy(Path(val, 'thumb.jpg'), Path(img_thumb, f'{RecipeName[i]}.jpg'))
            ImagePath[i] = f'{RecipeName[i]}.jpg'
    
    # save parsed JSON data as pickle
    with open(Path(Path.cwd(), 'RecipeData.pkl'), 'wb') as f:
        pickle.dump([RecipeName,RecipeCategory, PageName, JSONPath, ImagePath], f)
    return