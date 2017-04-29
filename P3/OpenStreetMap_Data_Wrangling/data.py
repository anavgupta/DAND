#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lxml.etree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

fault_nodes = []

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :

        # add all the attribute of the element in a key:value style
        attrib = element.attrib

        try:
        	node['id'] = attrib['id']
	        node['type'] = element.tag
	        if 'visible' not in attrib:
	            node['visible'] = "false"
	        else:
	            node['visible'] = attrib['visible']

	        node['created'] = {}
	        for k in CREATED:
	            node['created'][k] = attrib[k]

	        if element.tag == "node":
	            node['pos'] = []
	            node['pos'].append(float(attrib['lat']))
	            node['pos'].append(float(attrib['lon']))
        except KeyError as e:
            print str(e)
            fault_nodes.append(node)
         #    print element.tag
        	# print element.attrib

        # if there are 'tags' nodes present in the element
        for tag in element.iter("tag"):
            if problemchars.search(tag.attrib['k']):
                continue
            elif lower.search(tag.attrib['k']):
                node[tag.attrib['k']] = tag.attrib['v']
            elif lower_colon.search(tag.attrib['k']):
                keys = tag.attrib['k'].split(":")
                if len(keys) > 2:
                    continue
                else:
                    if keys[0] == "addr":
                        if 'address' not in node:
                            node['address'] = {}
                        node['address'][keys[1]] = tag.attrib['v']
                    else:
                        if keys[0] not in node:
                            node[keys[0]] = {}
                            node[keys[0]][keys[1]] = tag.attrib['v']
                        else:
                            if type(node[keys[0]]) is dict:
                                node[keys[0]][keys[1]] = tag.attrib['v']
                            else:
                                t_dict = {}
                                t_dict[keys[0]] = node[keys[0]]
                                t_dict[keys[1]] = tag.attrib['v']
                                node[keys[0]] = t_dict

        # if there are 'nd' nodes present in the element
        for nd in element.iter("nd"):
            if 'node_refs' not in node:
                node['node_refs'] = []
            node['node_refs'].append(nd.attrib['ref'])

        # print node
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('example.osm', True)
    #pprint.pprint(data)

    correct_first_elem = {
        "id": "261114295",
        "visible": "true",
        "type": "node",
        "pos": [41.9730791, -87.6866303],
        "created": {
            "changeset": "11129782",
            "user": "bbmiller",
            "version": "7",
            "uid": "451048",
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.",
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369",
                                    "2199822370", "2199822284", "2199822281"]

# if __name__ == "__main__":
#     test()
