from flask import Flask
import pymongo
import os
import Model

app = Flask(__name__)
link = "mongodb+srv://"+os.environ['dbuser']+":"+os.environ['dbpass']+"@cluster0.zltoe.mongodb.net/homeStorage?retryWrites=true&w=majority"
client = pymongo.MongoClient(link)

homeStorage = client.homeStorage
fridge = homeStorage.fridge
print(fridge)
m = Model.Food('m', 2)
print(m.name)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/get', methods=['GET'])
def hello_world2():
    return 'Hello World2'

@app.route('/post', methods=['POST'])
def add():
    fridge.insert_one({"name": m.name, "amount": m.amount})
    return '200'

if __name__ == '__main__':
    app.run()