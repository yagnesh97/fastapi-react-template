from typing import Any

from pymongo import MongoClient
from pymongo.database import Database

from app.config import settings


def get_db() -> Database[Any]:
    """
    Get MongoDB
    """
    if settings.ci:
        import mongomock

        return mongomock.MongoClient()[settings.mongo_db]

    return MongoClient(settings.mongo_uri)[settings.mongo_db]


db = get_db()
