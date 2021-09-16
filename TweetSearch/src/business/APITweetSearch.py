from src.business.Common import Common
from src.business.JsonToObj import jsonToObj
from src.data.MongoDB import MongoDB
from requests.exceptions import HTTPError, InvalidHeader
from bson import ObjectId
import json 
import urllib as url
import requests
import datetime

class APITweetSearch:
 
    data = list()
    users = list()
    places = list()

    def __init__(self, Search):
        self.search = Search
        self.query = Search['user_query']
        self.language =  Search['user_language'].split(' : ',1)[0]
        
    def getRecentTweets(self, NextToken) -> dict:
        
        Common.Configuration['Twitter_Search_Params']['query'] = f"{self.query} lang: {self.language} - is:retweet"
        Common.Configuration['Twitter_Search_Params']['next_token'] = NextToken
        if NextToken == '':
            del Common.Configuration['Twitter_Search_Params']['next_token']
        
        try:
            response = requests.get(Common.Configuration['Twitter_Authentication']['Twitter_URL_Recent_Search'], 
                                    params = Common.Configuration['Twitter_Search_Params'], 
                                    headers = Common.Configuration['Twitter_Authentication']['Twitter_Header'])

            TweetList = json.loads(response.content)

            if TweetList['meta']['result_count'] > 0:
                dt = datetime.datetime.now()
                if 'data' in TweetList:
                    self.data = TweetList['data']             
                    for d in self.data:
                        d['search_id'] = self.search['_id']
                        d['inserted_at'] = dt

                if 'users' in TweetList['includes']:
                    self.users = TweetList['includes']['users']           
                    for u in self.users:
                        u['_id'] = u['id']
                        del u['id']

                if 'places' in TweetList['includes']:
                    self.places = TweetList['includes']['places']           
                    for p in self.places:
                        p['_id'] = p['id']
                        del p['id']

            return TweetList
        except HTTPError as http_error:
            return (f'HTTP error: {http_error}')
        except InvalidHeader as invalid_header:
            return (f'URL error: {invalid_header}')
        except Exception as ex:
            return (f'Generic Error: {ex}')
            
    def InsertRecentSearch(self) -> bool:
        try:   
            Database = MongoDB()
            insTweets = Database.InsertItems(self.data, Common.Configuration['Database']['DB_TABLE_TWEET_DATA'])
            
            if self.users:
                insUsers = Database.InsertItems(self.users, Common.Configuration['Database']['DB_TABLE_TWEET_AUTHOR'])

            if self.places:
                insPlaces = Database.InsertItems(self.places, Common.Configuration['Database']['DB_TABLE_TWEET_PLACE'])

            return True
        except Exception as ex:
            return False            
    
 
