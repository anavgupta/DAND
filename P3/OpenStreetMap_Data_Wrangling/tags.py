#!/usr/bin/env python
# -*- coding: utf-8 -*-
from create_sample_data import get_element
import re

# regex to searh for types of tags
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.attrib['k']):
            keys['lower'] += 1
        elif lower_colon.search(element.attrib['k']):
            keys['lower_colon'] += 1
        elif problemchars.search(element.attrib['k']):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1

    return keys


# To process the OSM File for the tags
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for i, element in enumerate(get_element(filename)):
        keys = key_type(element, keys)

    return keys


# If the file is being run individually from the command prompt.
if __name__ == "__main__":
    filename = raw_input()
    data = process_map(filename)
    import pprint
    pprint.pprint(data)
