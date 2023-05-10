#!/usr/bin/env python3
""" tabulate logs """
from pymongo import MongoClient

# connect to MongoDB
client = MongoClient()
db = client.logs
collection = db.nginx

# count total number of logs
if __name__ == '__main__':
    total_logs = collection.count_documents({})

    # count number of logs with each HTTP method
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in http_methods:
        count = collection.count_documents({"method": method})
        method_counts[method] = count

    # count number of logs with method=GET and path=/status
    status_count = collection.count_documents({
        "method": "GET",
        "path": "/status"
    })

    # get top 10 IPs
    ip_counts = {}
    for log in collection.find():
        ip = log.get("ip")
        ip_counts[ip] = ip_counts.get(ip, 0) + 1
    top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    # print stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\t{method}: {count}")
    print(f"{status_count} status check")
    print("IPs:")
    for ip, count in top_ips:
        print(f"\t{ip}: {count}")
