#!/usr/bin/env python3

"""function that changes all topics of a school document based on the name:

    Prototype: def update_topics(mongo_collection, name, topics):
    mongo_collection will be the pymongo collection object
    name (string) will be the school name to update
    topics (list of strings) will be the list of topics in the school
"""


def update_topics(mongo_collection, name, topics):
    """perform update on mongodb collection object"""
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
