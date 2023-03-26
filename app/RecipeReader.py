from pathlib import Path
from flask import Blueprint, render_template, request, json
import pickle as pickle
from os import getenv
from .RecipeParser import RecipeParser

# Path to read and parse recipe data, defaults to bounded volume
path = Path(Path.cwd(), 'recipe_data')

# Function to parse recipe data, refresh to parse recipe folder if changes are made
def Refresh():
    RecipeParser(path)

# When starting: parse data, save variables in pickle
if not(Path(Path.cwd(), 'RecipeData.pkl').exists()):
    Refresh()

#Load in Environmental Variables
HomePageTitle =  getenv('PAGE_TITLE','Recipe Book')
LargeFont =  f'{getenv("FONT_LARGE","36")}px'
SmallFont =  f'{getenv("FONT_SMALL","30")}px'

imagetypeEnv = getenv('IMAGE_SIZE','Full')
if imagetypeEnv == 'Thumbnail':
    imagetype = 'thumbs'
else:
    imagetype = 'fulls'
del imagetypeEnv


bp = Blueprint('RecipeReader', __name__, url_prefix='/')
# Landing Page, list of recipes
# POST methods for refresh  or returning to category functions
@bp.route("/", methods = ['GET','POST'])
@bp.route("/recipes/", methods = ['GET','POST'])
def homepage():
    if request.method == 'POST':
        if request.form.get('reload') == 'Refresh List':
            Refresh()
        if request.form.get('cat-select') != None:
            ActiveCat = request.form.get('cat-select')
        else:
            ActiveCat = 'Show all'
    else:
        ActiveCat = 'Show all'
        
    with open(Path(Path.cwd(), 'RecipeData.pkl'), 'rb') as f:
        RecipeName, RecipeCategory, PageName, JSONPath, ImagePath = pickle.load(f)
    del f, JSONPath, ImagePath
    
    Categories = list(set(RecipeCategory.values())) # unique categories for filter buttons
    Categories.insert(0,'Show all') # Add show all button
    
    return render_template('landing.html', RecipeName=RecipeName, ActiveCat=ActiveCat, \
                           PageName=PageName, HomePageTitle=HomePageTitle, \
                           Categories=Categories, RecipeCategory=RecipeCategory)


# Recipes Page, gather data from JSON to serve to jinja template
@bp.route('/recipes/<page>', methods = ['GET','POST'])
def showpage(page):
    with open(Path(Path.cwd(), 'RecipeData.pkl'), 'rb') as f:
        RecipeName, RecipeCategory, PageName, JSONPath, ImagePath = pickle.load(f)
    del f
    index = PageName[page] # recipe index to fetch associated data
    title = RecipeName[index]
    category = RecipeCategory[index]
    del PageName, RecipeName, RecipeCategory
    
    if request.method == 'POST': # Change image path (thumb vs full) if button pressed
        if request.form.get('imswitch') == 'Reduce Image Size':
            image = f'thumbs/{ImagePath[index]}'
        elif request.form.get('imswitch') == 'Restore Image Size':
            image = f'fulls/{ImagePath[index]}'
            
    elif request.method == 'GET': # Provide default image size if not
        if index in ImagePath:
            image = f'{imagetype}/{ImagePath[index]}'
        else:
            image = ''
    del ImagePath
    
    with open(JSONPath[index],'r') as file: # Recipe data
        data = json.load(file)
    del file
    
    name = data["name"]
    description = data["description"]
    ingredients = data["recipeIngredient"]
    instructions = data["recipeInstructions"]
    
    reviews = []
    ratings = []
    avgrating = ''
    
    if 'review' in data:
        for i,val in enumerate(data['review']):
            base = ''
            if 'reviewRating' in val:
                rating = int(val['reviewRating']['ratingValue'])
                ratings.append(rating)
                base = base + f'({rating}/5) '
            if 'reviewBody' in val:
                base = base + val['reviewBody']
            elif 'description' in val:
                base = base + val['description']
            try:
                base = f' {base} ~{val["author"]["name"]}'
            except:
                pass
            
            reviews.append(base)
        
        if len(ratings) > 0:
            avgrating = sum(ratings)/len(ratings)
            del ratings
    else:
        reviews = ''
    
    return render_template('recipe.html', LargeFont=LargeFont, SmallFont=SmallFont, \
                           category=category, page=page, title=title, image=image, \
                           name=name, description=description, ingredients=ingredients, \
                           instructions=instructions, reviews=reviews, avgrating=avgrating)

@bp.route("/favicon.ico")
def favicon():
    image = "favicon.ico"
    return render_template('image.html', image=image)    
