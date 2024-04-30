#!/usr/bin/env python3
'''This script contains the definition for the coroutine "insert_school"'''
from typing import List, Optional

from bson.objectid import ObjectId
from pymongo.collection import Collection


def insert_school(mongo_collection: Collection,
                  **kwargs
                  ) -> Optional[ObjectId]:
    '''insert_school: inserts a new document in a collection based on <kwargs>

    mongo_collection: pymongo collection object
    Returns: the new _id
    '''
    result = mongo_collection.insert_one(kwargs)

    if result.acknowledged:
        return result.inserted_id
    return None
