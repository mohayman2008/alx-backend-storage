#!/usr/bin/env python3
'''This script contains the definition for the coroutine "schools_by_topic"'''


def schools_by_topic(mongo_collection, topic):
    '''schools_by_topic: returns the list of school having a specific <topic>

    mongo_collection: pymongo collection object
    topic: (string) topic searched for

    return: a cursor for the query result
    '''
    return mongo_collection.find({"topics": {"$elemMatch": {"$eq": topic}}})
