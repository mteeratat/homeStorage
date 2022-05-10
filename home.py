from flask import Flask, render_template, request, jsonify
import pymongo
import os

app = Flask(__name__)
link = "mongodb+srv://"+os.environ['dbuser']+":"+os.environ['dbpass']+"@cluster0.zltoe.mongodb.net/homeStorage?retryWrites=true&w=majority"
client = pymongo.MongoClient(link)

homeStorage = client.homeStorage
fridge = homeStorage.fridge

@app.route('/', methods=['GET'])
def index():
    response = fridge.find()
    res = [r for r in response]
    return render_template('index.html', res=res)

@app.route('/search', methods=['GET'])
def search():
    response = fridge.find({'name': request.args.get('name')})
    res = [r for r in response]
    return render_template('search.html', res=res)

@app.route('/add', methods=['GET','POST'])
def add():
    res = ""
    if request.method == 'POST':
        print('x')
        x = fridge.insert_one({'name': request.form['name'], 'amount': request.form['num']})
        if x.acknowledged:
            res = "Add complete"
        else: 
            res = "Incomplete"
    return render_template('add.html', res=res)

# @app.route('/get', methods=['GET'])
# def hello_world2():
#     return 'Hello World2'

# @app.route('/post', methods=['POST'])
# def add():
#     x = fridge.insert_one({"name": m.name, "amount": m.amount})
#     print(x.acknowledged)
#     print(request)
#     return '200'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)