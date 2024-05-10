
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

def store_in_mongo(myclient,data_collections, database='scopus_db', collection_name='scopus_collection'):
    db = myclient[database]
    collection = db[collection_name]
    try:
        collection.insert_many(data_collections)
    except DuplicateKeyError as e:
        print(f'Duplicate key error: {e}')
    