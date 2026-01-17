from pymongo import MongoClient

client = MongoClient('mongodb://172.17.0.1:27017')

db = client.projectdb
