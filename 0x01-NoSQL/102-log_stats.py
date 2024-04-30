#!/usr/bin/env python3
'''This script provides some stats about Nginx logs stored in MongoDB'''
from pymongo import MongoClient


def main():
    '''main: entry point'''

    client = MongoClient()
    nginx_logs = client.logs.nginx

    print(nginx_logs.count_documents({}), "logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx_logs.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    print(nginx_logs.count_documents({"method": "GET", "path": "/status"}),
          "status check")

    ips = nginx_logs.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$project": {"ip": "$_id", "count": 1, "_id": 0}},
        {"$sort": {"count": -1, "ip": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for ip in ips:
        print("\t{}: {}".format(ip.get("ip"), ip.get("count")))

    client.close()


if __name__ == "__main__":
    main()
