from src.business.JsonToObj import jsonToObj 
import json
import datetime 
import os.path as path

class Common():
    '''Common values and constants used over the project'''

    #app.config file source
    APP_CONFIG_FILE = 'conf\\app.config.json'
    Configuration = dict()
            
