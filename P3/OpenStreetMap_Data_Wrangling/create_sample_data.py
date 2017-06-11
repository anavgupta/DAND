#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
create_sample_data.py
This file is used to create a sample.osm file, a smaller file that contains the
content of the Original OSM file.
This sample.osm is created for the testing purpose.

The function 'get_element' is of utmost important here.
It has been used throughout the project
"""
import xml.etree.cElementTree as ET


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


def create(infile, outfile, k=5):
    with open(outfile, 'wb') as output:
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
