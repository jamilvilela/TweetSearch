from src.Common import Common
import json
import bson
from src.source.Tweet import jsonify
import pymongo 
from pymongo import MongoClient
from pymongo import ReturnDocument
from bson import ObjectId
import datetime


class ConnectMongoDB:
    """connection to the MongoDB database"""    

    def __init__(self):
        self._stringConn = (f'mongodb+srv://{Common.DB_USER_NAME}:{Common.DB_PASSWORD}@{Common.DB_CLUSTER_NAME}.n3igf.mongodb.net/{Common.DB_DATABASE_NAME}?retryWrites=true&w=majority')

        try:
            cluster = MongoClient(self._stringConn)
            self._db = cluster[Common.DB_DATABASE_NAME]            
        except Exception as ex:
            return (f'Database connection error: {ex}')
    
    def InsertItems(self, Items, Collection):
        try:
            coll = self._db[Collection]
         
            insList = coll.insert_many(Items)
            
            return insList
        except Exception as ex:
            return (f'Data insert error: {Collection}')
    
    def AppendFields(self, Filter, Update, Collection, Upsert):
        try:
            coll = self._db[Collection]

            updList = coll.update_many(Filter, Update, upsert=Upsert)
            return updList
        except Exception as ex:
            return(f'Data update error: {Collection}')

    def InsertRecentSearch(self, Search, Result) -> bool:
        try:   
            Common.Print_time('insert search...')

            insSearch = self.AppendFields(Search[0],
                                          {'$set': Search[0]},
                                          Common.DB_TABLE_USER_SEARCH,
                                          Upsert=True)
            
            data = Result['data']   
            
            #for i in data:
            #    i['search_id'] = ObjectId(insSearch[0])
            #    i['_id'] = i['id']
            #    i['inserted_at'] = dt_insert
            #    del i['id']
            Common.Print_time('insert search data.')

            insTweets = self.InsertItems(data, Common.DB_TABLE_TWEET_DATA)
            self.AppendFields({'_id': {'$in': insTweets.inserted_ids}}, 
                              {'$set': {'search_id': ObjectId(insSearch.upserted_id)}},
                               Common.DB_TABLE_TWEET_DATA,
                               Upsert=False)

            Common.Print_time('insert search users.')

            users = Result['includes']['users']           
            for i in users:
                i['_id'] = i['id']
                del i['id']

            insUsers = self.InsertItems(users, Common.DB_TABLE_TWEET_AUTHOR)

            Common.Print_time('Data insert has finished.')

            return True
        except Exception as ex:
            print(f'Result insert error: {ex}')
            return False
   