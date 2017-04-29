#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from collections import defaultdict
import xml.etree.cElementTree as ET
import re
import pprint

housenumber_re = re.compile(r'[a-zA-Z]+')

OSMFILE = 'sample.osm'

def is_housenumber(tag):
	return tag.attrib['k'] == 'addr:housenumber'

def audit_housenumber(housenubmer_types, housenumber):
	house_se = housenumber_re.search(housenumber)
	if house_se:
		housenubmer_type = house_se.group()
		housenubmer_types[housenubmer_type].add(housenumber)


def audit(filename):
	housenubmer_types = defaultdict(set)
	osm_file = open(filename, "r")

	for _, elem in ET.iterparse(osm_file):
			if elem.tag == "node" or elem.tag == "way":

				for tag in elem.iter("tag"):
					if is_housenumber(tag):
						audit_housenumber(housenubmer_types, tag.attrib['v'])
	return housenubmer_types

# def test():


# if __name__ == "__main__":
