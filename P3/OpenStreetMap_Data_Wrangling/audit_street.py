import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "sample.osm"
street_types_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def if_street_name(elem):
	return (elem.attrib['k'] == "addr:street")

def audit_street_type(street_types, street_name):
	m = street_types_re.search(street_name)

	if m:
		street_type = m.group()
		street_types[street_type].add(street_name)

def audit(osmfile):
	street_types = defaultdict(set)
	osm_file = open(osmfile, "r")

	for _, elem in ET.iterparse(osmfile):
		if elem.tag == "node" or elem.tag == "way":

			for tag in elem.iter("tag"):
				if if_street_name(tag):
					audit_street_type(street_types, tag.attrib['v'])

	return street_types

# if __name__ == "__main__":
# 	test()
