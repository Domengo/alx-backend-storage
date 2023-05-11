#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import requests


def wrapper(method: callable) -> callable:
    """wrapper"""
    def wrapped(url):
        """wrapped"""
        return method(url)
    return wrapped

def get_page(url: str) -> str:
    """get_page"""
    res = requests.get(url)
    return res.text
