from pymongo import MongoClient

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")


def get_mongo_client(uri: str = mongo_uri) -> MongoClient:
    return MongoClient(uri)
