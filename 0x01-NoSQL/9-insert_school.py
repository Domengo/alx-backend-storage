#!/usr/bin/env python3
"""_summary_ insert a document in Python"""


def insert_school(mongo_collection, **kwargs):
    """insert new documents"""
    return mongo_collection.insert_one(kwargs).inserted_id
