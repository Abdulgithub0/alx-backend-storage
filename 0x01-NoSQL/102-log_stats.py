#!/usr/bin/env python3

'''script that provides some stats about Nginx logs stored in MongoDB'''

from pymongo import MongoClient


if __name__ == '__main__':
    '''log the web traffic data store on the mongodb'''
    nginx = MongoClient().logs.nginx
    doc = nginx.count_documents({})
    if doc:
        print(doc, ' logs\nMethods:')
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        for val in methods:
            print('    method {}: {}'.format(val,
                  nginx.count_documents({'method': val})))
        print(nginx.count_documents({'path': '/status'}), ' status check')
        ips = nginx.aggregate([
            {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ])

        print('IPs:')
        for ip_info in ips:
            ip = ip_info['_id']
            count = ip_info['count']
            print(f'    {ip}: {count}')
