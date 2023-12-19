#!/usr/bin/env python3

"""Write a function that inserts a new docu into collection based on kwargs:

    Prototype: def insert_school(mongo_collection, **kwargs):
    mongo_collection will be the pymongo collection object
    Returns the new _id
"""


def insert_school(mongo_collection, **kwargs):
    """insert a doc and return it _id"""
    return mongo_collection.insert_one(kwargs).inserted_id
