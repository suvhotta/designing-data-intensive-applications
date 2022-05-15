from pymongo import MongoClient

from bson.objectid import ObjectId
from datetime import datetime

# connection_str = "mongodb+srv://<username>:<password>@suvsmongodb.1boby.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
connection_str = "mongodb+srv://suv:suv@suvsmongodb.1boby.mongodb.net/SuvsMongoDB?retryWrites=true&w=majority"

client = MongoClient(connection_str)

# print(client.list_database_names())

test_db = client.test

urls_collection = test_db.urls

print(urls_collection.find_one({"urlCode": "7uJhcthIR"}))

print(urls_collection.find_one({"_id": ObjectId('5fc1dfa13ea53d4eb449277d')}))

sample_url = {
    "urlCode": 'abcdef',
    'longUrl': 'abcdef.com',
    'shortUrl': 'kjl.com',
    'date': datetime.utcnow()
}

# result = urls_collection.insert_one(sample_url)
#
# print(result)
query_string = {'$regex': '.*kjl.*'}
print(urls_collection.find_one({'shortUrl': query_string}))


date = datetime(2018,2,2)
query_string = {'$gte': date}
print(urls_collection.find({'shortUrl': query_string}).sort("urlCode"))

# https://docs.mongodb.com/manual/reference/operator/query/eq/#mongodb-query-op.-eq