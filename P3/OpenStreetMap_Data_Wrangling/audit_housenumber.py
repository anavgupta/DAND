#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from collections import defaultdict
from create_sample_data import get_element
import codecs
import re

housenumber_re = re.compile(r'[\D]+')

OSMFILE = 'sample.osm'


#  Check whether the tag contains the housenumber or not.
def is_housenumber(tag):
    return tag.attrib['k'] == 'addr:housenumber'


# check whether the housenumbers contains letter or not
def audit_housenumber(housenubmer_types, housenumber):
    house_se = housenumber_re.search(housenumber)
    if house_se:
        housenubmer_type = house_se.group()
        housenubmer_types[housenubmer_type].add(housenumber)


# Audit the osm file for the housenumbers
def audit(filename):
    housenubmer_types = defaultdict(set)
    osm_file = open(filename, "r")

    for _, elem in enumerate(get_element(osm_file)):
        if elem.tag == "node" or elem.tag == "way":

            for tag in elem.iter("tag"):
                if is_housenumber(tag):
                    audit_housenumber(housenubmer_types, tag.attrib['v'])
    return housenubmer_types


# To start the testing process
def test(filename):
    data = audit(filename)
    hk = codecs.open('house_keys.txt', 'w')
    with codecs.open('audit_house.txt', 'w+') as f:
        f.write(housenumber_re.pattern + "\n")
        for key in data:
            hk.write(key + "\n")
            f.write(key + ": " + str(data[key]) + "\n")


# If the file is being run individually
if __name__ == "__main__":
    osmfile = raw_input()
    test(osmfile)
