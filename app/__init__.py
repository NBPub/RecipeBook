from flask import Flask
import logging
from os import getenv
from pathlib import Path

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

# recipes folder, could let user specify later
data_path = Path(Path.cwd(), 'recipe_data')

def create_app(test_config=None):
    app = Flask(__name__) # application factory
    
    # When starting: parse recipe data, and save as pickle
    if not(Path(Path.cwd(), 'RecipeData.pkl').exists()):
        from .RecipeParser import RecipeParser
        check = RecipeParser(data_path, app)
    else:
        check = True
    # Provide error page if no recipe data found
    if not check:
        from . import NoData
        app.register_blueprint(NoData.bp)
        return app
    
    # register main Blueprint
    from . import RecipeReader
    app.register_blueprint(RecipeReader.bp)
    
    # register API if enabled
    enable_api =  getenv('ENABLE_API', False)
    if type(enable_api) == str and enable_api.lower() == 'true':
        from . import api_v1
        app.register_blueprint(api_v1.bp)
        app.logger.info('API enabled at */api/info') 
    else:
        app.logger.info('API disabled, set "ENABLE_API=True" to enable') 
    
    app.logger.info('. . . starting RecipeBook . . .')  
    if not app.debug: 
        app.logger.setLevel(logging.INFO) # adjust later
    else:
        app.logger.setLevel(logging.INFO) 
    return app