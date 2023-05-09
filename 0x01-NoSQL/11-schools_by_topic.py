#!/usr/bin/env python3
""" 11-main """


def schools_by_topic(mongo_collection, topic):
    """find topic"""
    return [school for school in mongo_collection.find({"topic": {"$elemMatch": {"$eq": topic}}})]
