#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET

k = 50

def get_element(osm_file, tags=('node', 'way', 'relation')):
	"""Yeild element if it is the right type of tag

	Reference:
	http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-
generated-via-xml-etree-elementtree-in-python
	"""

	context = iter(ET.iterparse(osm_file, events=('start', 'end')))
	_, root = next(context)
	for event, elem in context:
		if event == 'end' and elem.tag in tags:
			yield elem
			root.clear()


def create(infile, outfile):
	with open (outfile, 'wb') as output:
		output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		output.write('<osm>\n   ')

		# write every kth top level element
		for i, element in enumerate(get_element(infile)):
			if i % k == 0:
				output.write(ET.tostring(element, encoding='utf-8'))

		output.write('</osm>')

if __name__ == "__main__":
	OSM_FILE = 'birmingham_england.osm'
	SAMPLE_FILE = 'sample.osm'
	create(OSM_FILE, SAMPLE_FILE)
