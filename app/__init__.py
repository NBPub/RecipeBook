from flask import Flask
import logging
from os import getenv

def create_app(test_config=None):
    app = Flask(__name__) # FLASK_APP configured via environmental variables
    
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
        app.logger.setLevel(logging.ERROR) # adjust later
    else:
        app.logger.setLevel(logging.INFO) 
    return app