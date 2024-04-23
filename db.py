from flask import Flask
from flask_pymongo import pymongo


CONNECTION_STRING = "mongodb+srv://judy:sda2024@sda.eazec5h.mongodb.net/?retryWrites=true&w=majority&appName=SDA"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database("sda")
groupContact_collection = pymongo.collection.Collection(db, "groupContact")
individualContact_collection = pymongo.collection.Collection(db, "individualContact")
contacts_collection = pymongo.collection.Collection(db, "contacts")