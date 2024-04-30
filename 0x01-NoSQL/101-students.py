#!/usr/bin/env python3
'''This module contains the definition for the function "top_students"'''


def top_students(mongo_collection):
    '''top_students: returns all students sorted by average score
    in descending order

    mongo_collection: pymongo collection object
    topic: (string) topic searched for

    return: a cursor for the query results, including key <averageScore>
    '''
    return mongo_collection.aggregate([
        {"$addFields":
         {"averageScore": {"$avg": "$topics.score"}
          }
         },
        {"$sort": {"averageScore": -1}}
    ])
