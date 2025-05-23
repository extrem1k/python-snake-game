import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def get_database():
    """
    Łączy się z bazą danych MongoDB.
    """
    MONGO_URI = os.getenv("MONGO_URI")
    DATABASE_NAME = "extrem1k"

    if not MONGO_URI:
        raise ValueError("Brak zmiennej środowiskowej MONGO_URI.")

    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db
