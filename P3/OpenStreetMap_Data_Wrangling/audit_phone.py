import re
import json
import pprint

phone_re = re.compile(r'[\w+]?\b')

def get_db(db_name):
	from pymongo import MongoClient
	client = MongoClient('localhost:27017')
	db = client[db_name]
	return db

def aggregate(db, collection, pipeline):
	[doc for doc in db.collection.aggregate(pipeline)]

def make_pipeline():
	pipeline = [
		{"$exits" : {"amnesty" : 1}}
	]
	return pipeline

def make_query():
	query = {

	}
