#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
users.py
This file is used to create a set of the Users
"""
from create_sample_data import get_element


# To get the user id
def get_user(element):
    return element.attrib['uid']


# To Process the OSM File
def process_map(filename):
    users = set()

    for i, element in enumerate(get_element(filename)):
        try:
            if element.tag in ["node", "way", "relation"]:
                user_id = get_user(element)
                users.add(user_id)
        except KeyError as e:
            print e
    return users


# If the file is being run individually from the command prompt.
if __name__ == "__main__":
    filename = raw_input()
    data = process_map(filename)
    import pprint
    pprint.pprint(data)
    pprint.pprint(len(data))
