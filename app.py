from flask import Flask, jsonify, Blueprint
# from flask_jwt_extended import JWTManager
from pymongo.mongo_client import MongoClient
from controllers.contactController import contact_blueprint
import db
from pymongo.server_api import ServerApi
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# app.config['JWT_SECRET_KEY'] = '666'
# jwt = JWTManager(app)
app.register_blueprint(contact_blueprint, url_prefix='/')

@app.route('/')
def home():
    return 'Hello, Flask!'

uri = "mongodb+srv://judy:sda2024@sda.eazec5h.mongodb.net/?retryWrites=true&w=majority&appName=SDA"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

if __name__ == '__main__':
    app.run(debug=True)
