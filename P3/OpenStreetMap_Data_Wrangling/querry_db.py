from lxml import etree as ET
import re
import json


def get_db(db_name):
	from pymongo import MongoClient
	client = MongoClient('localhost:27017')
	db = client[db_name]
	return db

def aggregate(db, collection, pipeline):
	return [doc for doc in db.sample.aggregate(pipeline)]

def find(db, collection, query, projection=None):
	return [doc for doc in db.sample.find(query, projection)]
	# return db.collection.find(query)

def make_pipeline():
	pipeline = [
		{ $group : { "_id" : { "housenumber" : '$address.housenumber', \
			'postcode' : '$address.postcode'}, 'count' : {'$sum' : 1} }
		}
	]
	return pipeline

def make_query():
	query = {
		# 'phone' : {"$regex" : '^(\+44)|^(01)|^(02)'}
		'address.housenumber' : {'$exists' : 1}
	}
	return query

def make_projection():
	projection = {
	'phone' : 1,
	'amenity' : 1,
	'type' : 1,
	'address.housenumber' : 1,
	'address.postcode' : 1
	}
	return projection

# if __name__ == "__main__":
# 	db = get_db('examples')
# 	# pipeline = make_pipeline()
# 	query = make_query()
# 	projection = make_projection()
# 	result = find(db, 'sample', query, projection)
# 	import pprint
# 	# result_list = [doc for doc in result]
# 	pprint.pprint(result)
# 	pprint.pprint(len(result))

