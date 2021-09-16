from src.business.Common import Common
from src.data.MongoDB import MongoDB
from requests.exceptions import HTTPError, InvalidHeader
from bson import ObjectId
import json 
import urllib as url
import requests
import datetime

class APIAppClient:
    '''data extraction from the App Twitr Whatever'''

    AppSearchList = list()
 
    def get_User_Search(self) -> dict:
        dt = datetime.datetime.now()

        try:
            response = requests.get(Common.Configuration['App_User_Search']['url'])
            content = json.loads(response.content)
            data = content['response']['results']
            for i in data:
                del i['Created By']
                del i['Modified Date']
                i['inserted_at'] = dt
            
            self.AppSearchList = data
            return self.AppSearchList

        except HTTPError as http_error:
            return (f'HTTP error: {http_error}')
        except InvalidHeader as invalid_header:
            return (f'URL error: {invalid_header}')
        except Exception as ex:
            return (f'Generic Error: {ex}')
            
    def Insert_user_search(self) -> bool:
        try:
            DataBase = MongoDB()
            for Search in self.AppSearchList:
                insSearch = DataBase.UpdateItems({'_id': Search['_id']},
                                                 {'$set': Search},
                                                 Common.Configuration['Database']['DB_TABLE_USER_SEARCH'],
                                                 Upsert=True)
            return True
        except Exception as ex:
            return False

    def Update_user_search(self, Search_ID_List):
        try:
            DataBase = MongoDB()
            insSearch = DataBase.UpdateItems({'_id': {'$in': Search_ID_List}},
                                              {'$set': {'integrated_at': datetime.datetime.now()}},
                                              Common.Configuration['Database']['DB_TABLE_USER_SEARCH'],
                                              Upsert=False)
            return True
        except Exception as ex:
            return False
 
    def Not_Integrated_Search(self) -> list:
        try:
            DataBase = MongoDB()
            return DataBase.Find({'integrated_at':None}, Common.Configuration['Database']['DB_TABLE_USER_SEARCH'])
        except Exception as ex:
            return False

    def Get_App_data(self) -> bool:
        self.get_User_Search()
        return self.Insert_user_search()
