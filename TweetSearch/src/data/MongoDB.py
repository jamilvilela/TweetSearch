from src.business.Common import Common
from src.business.JsonToObj import jsonToObj
from pymongo import MongoClient
from pymongo import ReturnDocument
import pymongo
import json
import bson
import datetime


class MongoDB:
    """connection to the MongoDB database"""    

    def __init__(self):
        self.user = Common.Configuration['Database']['DB_USER_NAME']
        self.password = Common.Configuration['Database']['DB_PASSWORD']
        self.cluster = Common.Configuration['Database']['DB_CLUSTER_NAME']
        self.database = Common.Configuration['Database']['DB_DATABASE_NAME']
        self._stringConn = (f'mongodb+srv://{self.user}:{self.password}@{self.cluster}.n3igf.mongodb.net/{self.database}?retryWrites=true&w=majority')

        try:
            cluster = MongoClient(self._stringConn)
            self._db = cluster[self.database]            
        except Exception as ex:
            return (f'Database connection error: {ex}')
    
    def Find(self, Filter, Collection) -> list:
        try:
            coll = self._db[Collection]
            listFound = coll.find(Filter)
            return listFound
        except Exception as ex:
            return(f'Find error {Collection}')


    def InsertItems(self, Items, Collection):
        """ Insert a set of documents"""
        try:
            coll = self._db[Collection]
         
            insList = coll.insert_many(Items)
            
            return insList
        except Exception as ex:
            return (f'Data insert error: {Collection}')
    
    def UpdateItems(self, Filter, Update, Collection, Upsert):
        """ Update a set of documents"""
        try:
            coll = self._db[Collection]

            updList = coll.update_many(Filter, Update, upsert=Upsert)
            return updList
        except Exception as ex:
            return(f'Data update error: {Collection}')


   