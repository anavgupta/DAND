#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
audit_street.py
This file is used to analyze the street names in the OSM file
This file is run individually and comes in the auditing process phase.
"""
from collections import defaultdict
from create_sample_data import get_element
import re
# import pprint

OSMFILE = "sample.osm"
street_types_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


# chech whether the tag is about the street name or not
def if_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


# Add the street type with the street name
def audit_street_type(street_types, street_name):
    m = street_types_re.search(street_name)

    if m:
        street_type = m.group()
        street_types[street_type].add(street_name)


# Audit the osm file for the street names
def audit(osmfile):
    street_types = defaultdict(set)
    for i, elem in enumerate(get_element(osmfile)):
        if elem.tag == "node" or elem.tag == "way":

            for tag in elem.iter("tag"):
                if if_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


# To start the testing process
def test(filename):
    data = audit(filename)
    with open('audit_street.txt', 'w') as f:
        f.write(street_types_re.pattern + "\n")
        for key in data:
            f.write(key + ': ' + str(data[key]) + '\n')
    # json.dump(data, open('audit_street.txt', 'w'))


# If the file is being run individually
if __name__ == "__main__":
    osmfile = raw_input()
    test(osmfile)
