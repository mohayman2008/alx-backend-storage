#!/usr/bin/env python3
'''This script contains the definition for the coroutine "list_all"'''


def list_all(mongo_collection):
    '''list_all: lists all documents in a MongoDB collection'''
    if not mongo_collection.count_documents({}):
        return []
    return mongo_collection.find()
