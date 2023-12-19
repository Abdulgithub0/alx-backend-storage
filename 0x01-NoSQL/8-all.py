#!/usr/bin/env python3

"""display all documents present in input collections"""


def list_all(mongo_collection):
    """list and display docs"""
    return [ d for d in mongo_collection.find()]
