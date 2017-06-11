#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mapparser.py
This file is used to calculate the tags and their count in an OSM file.
"""
from create_sample_data import get_element


# To count the tags present in the OSM file.
def count_tags(filename):
    tags = {}

    for i, elem in enumerate(get_element(filename)):
        # print elem.tag
        if elem.tag in tags:
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1

    return tags


# If the file is being run Individually
if __name__ == "__main__":
    filename = raw_input()
    data = count_tags(filename)
    import pprint
    pprint.pprint(data)
