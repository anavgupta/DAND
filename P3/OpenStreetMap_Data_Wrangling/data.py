#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the main file that is used in the final data cleaning process of the
OSM file.
It cleans and create a JSON file from the OSM file
"""

# To import all the necessary libraries
from create_sample_data import get_element
import audit
import update
import re
import codecs
import json

# This is data created after after the first processing cycle
data_created_1 = {
    "relief": 1,
    "statue": 1,
    "Estate Agents": 1,
    "Monkey Puzzle": 1,
    "audio": 1,
    "Truvelo": 1,
    "security": 2,
    "K6": 3,
    "deciduous": 207,
    "broad_leafed": 13,
    "Sewage Pumping Station": 1,
    "sculpture": 2,
    "clothing;shoes": 1,
    "Chinese": 2,
    "plastic": 11,
    "broadleaved": 1,
    "surface": 1,
    "underground": 1,
    "concrete": 4,
    "sos": 42,
    "phone_mast": 1,
    "conifer": 11,
    "NDB": 1,
    "dog_waste": 3,
    "broad_leaved": 310,
    "node": 3884271,
    "VOR/DME": 1,
    "broad_leaf": 2
}

# This is data created after after the second processing cycle
data_created_2 = {
    "barracks": 1,
    "drain": 3,
    "checkout": 19,
    "broad_leaf": 2,
    "node": 6360317,
    "isle": 45,
    "broad_leaved": 356,
    "dog_waste": 3,
    "dance": 1,
    "NDB": 1,
    "phone_mast": 1,
    "way": 582248,
    "fuels": 2,
    "water": 23,
    "surface": 2,
    "underground": 1,
    "broadleaved": 1,
    "plastic": 11,
    "sos": 42,
    "puffin": 2,
    "clothing;shoes": 1,
    "Primary": 1,
    "oil": 3,
    "Sewage Pumping Station": 1,
    "deciduous": 210,
    "K6": 3,
    "security": 2,
    "route": 5,
    "moat": 1,
    "sculpture": 2,
    "audio": 1,
    "Monkey Puzzle": 1,
    "conifer": 12,
    "Estate Agents": 1,
    "VOR/DME": 1,
    "sewage": 1,
    "Chinese": 2,
    "statue": 2,
    "kiosk": 1,
    "broad_leafed": 13,
    "Truvelo": 1,
    "relief": 4,
    "gas": 16,
    "polish": 1,
    "concrete": 4,
    "fuel": 2,
    "Ambulance Station": 1,
    "towpath": 3,
    "multipolygon": 4,
    "chalet": 59,
    "spiral": 1
}

# This is data created after after the final processing cycle
data_created_final = {
    "heating": 1,
    "preserved": 1,
    "barracks": 1,
    "drain": 11,
    "checkout": 19,
    "broad_leaf": 2,
    "node": 6360317,
    "isle": 45,
    "broad_leaved": 356,
    "dog_waste": 3,
    "dance": 1,
    "NDB": 1,
    "phone_mast": 1,
    "way": 1067560,
    "fuels": 12,
    "water": 27,
    "surface": 2,
    "underground": 1,
    "broadleaved": 1,
    "plastic": 11,
    "sos": 42,
    "puffin": 2,
    "clothing;shoes": 1,
    "Primary": 1,
    "oil": 3,
    "Sewage Pumping Station": 1,
    "deciduous": 210,
    "K6": 3,
    "security": 2,
    "route": 6,
    "moat": 1,
    "sculpture": 2,
    "audio": 1,
    "Monkey Puzzle": 1,
    "conifer": 12,
    "Estate Agents": 1,
    "VOR/DME": 1,
    "sewage": 1,
    "Chinese": 2,
    "statue": 2,
    "kiosk": 1,
    "broad_leafed": 13,
    "Truvelo": 1,
    "relief": 4,
    "gas": 19,
    "polish": 1,
    "concrete": 4,
    "fuel": 4,
    "site": 1,
    "Ambulance Station": 1,
    "towpath": 5,
    "multipolygon": 6,
    "chalet": 59,
    "spiral": 1,
}

# To form regex for classifying the tag into three categories.
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]

# A Dict to contain all the nodes that throw exception.
fault_nodes = []


# A function to split the values into a list if it seperated by a semicolon
# def assign_values(value):
#     if value.find(';') != -1:
#         return [x.strip() for x in value.split(';')]


# To shape the final document in the predefined way
def shape_element(element):
    node = {}

    if element.tag == "node" or element.tag == "way":

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

        # if there are 'tag' nodes present in the element
        for tag in element.iter("tag"):

            # If the tag's key attrib contains problem chars, continue
            if problemchars.search(tag.attrib['k']):
                continue

            # if the tag's key attrib contains single word eg "visible"
            elif lower.search(tag.attrib['k']):
                # node[tag.attrib['k']] = assign_values(tag.attrib['v'])
                node[tag.attrib['k']] = tag.attrib['v']

            # if the tag's key attrib contains two words seperated by colon
            elif lower_colon.search(tag.attrib['k']):
                keys = tag.attrib['k'].split(":")

                if len(keys) > 2:
                    continue

                else:
                    if keys[0] == "addr":

                        # create a dict in the node if not alread created
                        if 'address' not in node:
                            node['address'] = {}

                        value = tag.attrib['v']

                        # Add the street into the node. Audit it and update it if necessary.
                        if keys[1] == 'street':
                            audit_result = audit.audit_street(value)
                            if(audit_result):
                                value = update.update_street(value, audit_result.group())
                                # print '1'

                        # Add the housenubmers into the node. Audit it and update it if necessary.
                        elif keys[1] == 'housenumber':
                            audit_result = audit.audit_housenumber(value)
                            if(audit_result):
                                value = update.update_housenumber(value, audit_result.group())
                                # print '2'

                        # node['address'][keys[1]] = assign_values(value)
                        node['address'][keys[1]] = value

                    else:
                        # If the key is not yet present in the node.
                        if keys[0] not in node:
                            node[keys[0]] = {}
                            # node[keys[0]][keys[1]] = assign_values(tag.attrib['v'])
                            node[keys[0]][keys[1]] = tag.attrib['v']
                        else:

                            # if the key is present in the node but it is a Dictionary
                            if type(node[keys[0]]) is dict:
                                # node[keys[0]][keys[1]] = assign_values(tag.attrib['v'])
                                node[keys[0]][keys[1]] = tag.attrib['v']

                            # if the node is present in the node but it is not a dictionary
                            # Then create a dictionary with the same name and add the value to this dictionary.
                            # eg: 'building' : yes and 'building:type' : Commercial
                            else:
                                t_dict = {}
                                t_dict[keys[0]] = node[keys[0]]
                                # t_dict[keys[1]] = assign_values(tag.attrib['v'])
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


# Controller function that create the json file by calling the shape element for all the nodes in the OSM File
def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "a") as fo:
        for i, element in enumerate(get_element(file_in)):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")

            # To make sure that my file fully processed
            # if i < 3884897, File first stopped processing after this no of lines
            # if i < 6943441: File second stopped processing after this no of lines
            #     continue
            # else:
            #     el = shape_element(element)
            #     if el:
            #         data.append(el)
            #         if pretty:
            #             fo.write(json.dumps(el, indent=2) + "\n")
            #         else:
            #             fo.write(json.dumps(el) + "\n")
    return data


# If the file is being run individually from the command prompt.
if __name__ == "__main__":
    filename = raw_input()
    process_map(filename)
