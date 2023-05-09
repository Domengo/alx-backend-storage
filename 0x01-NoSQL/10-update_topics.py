#!/usr/bin/env python3
""" 10-main """


def update_topics(mongo_collection, name, topics):
    """update topics"""
    query = {'name': name}
    new_values = {'$set': {'topics': topics}}
    result = mongo_collection.update_many(query, new_values)
    return result.modified_count
