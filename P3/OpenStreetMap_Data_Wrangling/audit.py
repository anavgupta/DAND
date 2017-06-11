#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is used to audit the values according to a predefined pattern and
return the searhc result.

This file is used in the final data cleaning process
"""

# Import the regex library
import re

# An Object to hold the regex for all the variable to be seached
tag_re = {
    'street': re.compile(r'\b\S+\.?$', re.IGNORECASE),
    'housenumber': re.compile(r'[\D]+')
}

# An Object to contain the tag's key value for a tag's type.
tag_type = {
    'housenumber': 'addr:housenumber',
    'street': 'addr:street'
    # 'phone': 'phone',
    # 'postcode': 'addr:postcode'
}


# def audit_tag_value(tag_value_types, tag_value):


# Check the type of the Tag Attribute
def check_tag_type(tag, type):
    if type in tag_type:
        return (tag.attrib['k'] == tag_type[type])


# To search the housenumbers using the regex stored in the tag_re object
def audit_housenumber(elem):
    m = tag_re['housenumber'].search(elem)
    return m


# To search the streets using the regex stored in the tag_re object
def audit_street(elem):
    m = tag_re['street'].search(elem)
    return m
