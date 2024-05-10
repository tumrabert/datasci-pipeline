import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def connect_to_mongo():
    try:
        MONGO_CONNECT = os.getenv("mongo_connect")
        client = MongoClient(MONGO_CONNECT)
        print("Connect successfully")
        return client
    except Exception as e:
        print("Connect Failed")
        return False
