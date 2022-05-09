from flask import Flask, render_template, request
import pymongo
import os
from static import Model

app = Flask(__name__)
link = "mongodb+srv://"+os.environ['dbuser']+":"+os.environ['dbpass']+"@cluster0.zltoe.mongodb.net/homeStorage?retryWrites=true&w=majority"
client = pymongo.MongoClient(link)

homeStorage = client.homeStorage
fridge = homeStorage.fridge
print(fridge)
m = Model.Food('m', 2)
print(m.name)

@app.route('/', methods=['GET'])
def index():
    print(request)
    return render_template('index.html')

@app.route('/', methods=['POST'])
def search():
    print(request)
    if request.form['name'] != '':
        print(request.form['name'])
    return render_template('index.html')

@app.route('/get', methods=['GET'])
def hello_world2():
    return 'Hello World2'

@app.route('/post', methods=['POST'])
def add():
    x = fridge.insert_one({"name": m.name, "amount": m.amount})
    print(x.acknowledged)
    print(request)
    return '200'

if __name__ == '__main__':
    app.run(host='0.0.0.0')