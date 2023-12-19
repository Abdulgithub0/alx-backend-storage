#!/usr/bin/env python3

"""perform sorting and average of scores"""


def top_students(mongo_collection):
    """return sorted score of students"""
    return mongo_collection.aggregate([
            {'$project': {'name': '$name',
             'averageScore': {'$avg': '$topics.score'}}},
            {'$sort': {'averageScore': -1}}
    ])
