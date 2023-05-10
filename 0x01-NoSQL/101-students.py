#!/usr/bin/env python3
""" 101-students.py """

def top_students(mongo_collection):
    """return top student"""
    pipeline = [
        {
            '$project': {
                'name': 1,
                'scores': 1,
                'averageScore': { '$avg': '$scores.score' }
            }
        },
        {
            '$sort': {
                'averageScore': -1
            }
        }
    ]
    return list(mongo_collection.aggregate(pipeline))
