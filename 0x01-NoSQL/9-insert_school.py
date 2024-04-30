#!/usr/bin/env python3
'''This module contains the definition for the function "insert_school"'''


def insert_school(mongo_collection, **kwargs):
    '''insert_school: inserts a new document in a collection based on <kwargs>

    mongo_collection: pymongo collection object

    Returns: the new _id
    '''
    result = mongo_collection.insert_one(kwargs)

    if result.acknowledged:
        return result.inserted_id
