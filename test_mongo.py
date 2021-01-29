from pymongo import MongoClient

client = MongoClient("mongodb://192.168.0.211:27017") 

db = client['urbandictionarytest']
print(db.name)

db['terms'].save({"title": "test"})