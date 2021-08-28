from src.Common import Common
import numpy as np
import json 
import urllib as url
import requests
from src.source.Tweet import jsonify
from requests.exceptions import HTTPError, InvalidHeader

class APITweetSearch:
 
    def __init__(self, query, language):
        self.__query = query
        self.__language = language
 
    @property
    def query(self):
        return self.__query

    @query.setter
    def query(self, query) -> str:
        if (query == null):
            raise 'Query have not defined.'
        else:
            self.query = query

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, language) -> str:
        if (language == null):
            raise 'Language have not defined.'
        else:
            self.language = language

    def getRecentTweets(self, NextToken) -> dict:
        
        Common.Twitter_Params['query'] = f"{self.query} lang: {self.language} - is:retweet"
        Common.Twitter_Params['next_token'] = NextToken
        if NextToken == '':
            Common.Twitter_Params.pop('next_token')
        
        try:
            #dicParams = self.encodeParams(Common.Twitter_Params)
            response = requests.get(Common.Twitter_URL_Recent_Search, 
                                    params=Common.Twitter_Params, 
                                    headers=Common.Twitter_Header)
            
            #TweetList = self.bindTweets(response.json())
            TweetList = json.loads(response.content)
         
            return TweetList

        except HTTPError as http_error:
            return (f'HTTP error: {http_error}')
        except InvalidHeader as invalid_header:
            return (f'URi error: {invalid_header}')
        except Exception as ex:
            return (f'Generic Error: {ex}')
            
            
    
 
