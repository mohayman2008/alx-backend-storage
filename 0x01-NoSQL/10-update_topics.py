#!/usr/bin/env python3
'''This script contains the definition for the coroutine "update_topics"'''


def update_topics(mongo_collection, name, topics):
    '''update_topics: changes all <topics> of a `school` document based on
    <name>

    mongo_collection: pymongo collection object
    name: (string) the school name to update
    topics: (list of strings) the list of topics approached in the school
    '''
    return mongo_collection.update_many({"name": name},
                                        {"$set": {"topics": topics}})
