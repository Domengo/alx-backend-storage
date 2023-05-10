#!/usr/bin/env python3
""" 101-students.py """


def top_students(mongo_collection):
    """return top student"""
    pipeline = [{"$project": {"_id": 1, "name": 1,
                            "averageScore": {
                                "$avg": {
                                    "$avg": "$topics.score", },
                                }, "topics": 1, }, },
                {"$sort": {"averageScore": -1}, }, ]
    return list(mongo_collection.aggregate(pipeline))
