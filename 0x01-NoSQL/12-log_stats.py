#!/usr/bin/env python3

"""script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def stat_logger():
    """log the web traffic data store on the mongodb"""
    nginx = MongoClient().logs.nginx
    print(nginx.count_documents({}), ' logs\nMethods:')
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for val in methods:
        print('\tmethod {}: {}'.format(val,
              nginx.count_documents({'method': val})))
    print(nginx.count_documents({'path': '/status'}), ' status check')


stat_logger()
