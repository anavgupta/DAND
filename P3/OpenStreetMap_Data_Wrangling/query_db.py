#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Query_db.py
This file is used to query the monogdb database
It is uses seperately after the data has been imported into the database
"""
import codecs
import json


# Get the name of the Database
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


# To run the MongoDB's aggregate command and return a list of documents returned
def aggregate(db, pipeline):
    return [doc for doc in db.birmingham.aggregate(pipeline)]


# To run the MongoDB's find command and return a list of all documents returned
def find(db, query, projection=None):
    return [doc for doc in db.birmingham.find(query, projection)]


# To create a pipleine for the aggregate command
def make_pipeline():
    pipeline = [
        {'$group': {'_id': '$source', 'Count': {'$sum': 1}}},
        {'$sort': {'Count': -1}}
    ]
    return pipeline


# Create a query
def make_query():
    query = {
        # 'phone' : {"$regex" : '^(\+44)|^(01)|^(02)'}
        'address.housenumber': {'$exists': 1}
    }
    return query


# creates Projection document
def make_projection():
    projection = {
        'phone': 1,
        'amenity': 1,
        'type': 1,
        'address.housenumber': 1,
        'address.postcode': 1
    }
    return projection


# If the file is run Individually
if __name__ == "__main__":
    db = get_db('osm')
    pipeline = make_pipeline()
    result = aggregate(db, 'sample', pipeline)
    with codecs.open('query_db.txt', 'w') as f:
        for doc in result:
            f.write(json.dumps(doc) + "\n")

# {'node': 6361009, 'relation': 7122, 'way': 1067779}
