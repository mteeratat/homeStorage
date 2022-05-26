from flask import Flask, redirect, render_template, request, jsonify, url_for
import pymongo
import os
import json
from datetime import datetime
import requests

app = Flask(__name__)
link = "mongodb+srv://"+os.environ['dbuser']+":"+os.environ['dbpass']+"@cluster0.zltoe.mongodb.net/homeStorage?retryWrites=true&w=majority"
client = pymongo.MongoClient(link)
linetoken = os.environ['linetoken']

homeStorage = client.homeStorage
fridge = homeStorage.fridge

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if request.form.get('increase') != None:
            temp = request.form.get('increase')
            temp2 = temp.split('-')
            amount = str(int(temp2[1]) + 1)
            r = fridge.update_one(filter={'name': temp2[0], 'amount': temp2[1]}, update={'$set': {'name': temp2[0], 'amount': amount}})
            print(r.raw_result)
        elif request.form.get('decrease') != None:
            temp = request.form.get('decrease')
            temp2 = temp.split('-')
            amount = str(int(temp2[1]) - 1)
            r = fridge.update_one(filter={'name': temp2[0], 'amount': temp2[1]}, update={'$set': {'name': temp2[0], 'amount': amount}})
            print(r.raw_result)
        elif request.form.get('delete') != None:
            temp = request.form.get('delete')
            temp2 = temp.split('-')
            r = fridge.delete_one({'name': temp2[0], 'amount': temp2[1]})
            print(r.raw_result)
        return redirect(url_for('index'))
    response = fridge.find()
    res = [r for r in response]
    return render_template('index.html', res=res)

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        print(request.form)
        if request.form.get('increase') != None:
            temp = request.form.get('increase')
            temp2 = temp.split('-')
            amount = str(int(temp2[1]) + 1)
            r = fridge.update_one(filter={'name': temp2[0], 'amount': temp2[1]}, update={'$set': {'name': temp2[0], 'amount': amount}})
            print(r.raw_result)
        elif request.form.get('decrease') != None:
            temp = request.form.get('decrease')
            temp2 = temp.split('-')
            amount = str(int(temp2[1]) - 1)
            r = fridge.update_one(filter={'name': temp2[0], 'amount': temp2[1]}, update={'$set': {'name': temp2[0], 'amount': amount}})
            print(r.raw_result)
        elif request.form.get('delete') != None:
            temp = request.form.get('delete')
            temp2 = temp.split('-')
            r = fridge.delete_one({'name': temp2[0], 'amount': temp2[1]})
            print(r.raw_result)
        # return redirect(url_for('search'))
        name = request.form.get('name')
        response = fridge.find(filter={'name': {"$regex": '.*'+name+'.*'}})
        res = [r for r in response]
        return render_template('search.html', res=res, name=name)

    name = request.args.get('name')
    # response = fridge.find(filter={'name': request.args.get('name')})
    response = fridge.find(filter={'name': {"$regex": '.*'+name+'.*'}})
    res = [r for r in response]
    return render_template('search.html', res=res, name=name)

@app.route('/add', methods=['GET','POST'])
def add():
    res = ""
    if request.method == 'POST':
        print('x')
        x = fridge.insert_one({'name': request.form['name'], 'amount': request.form['num'], 'expired': request.form['expired']})
        if x.acknowledged:
            res = "Add complete"
        else: 
            res = "Incomplete"
    return render_template('add.html', res=res)

@app.route('/expired', methods=['GET'])
def expired():
    response = fridge.find()
    res = [r for r in response]
    res2 = []
    for r in res:
        datetime_object = datetime.strptime(r['expired'], '%Y-%m-%d')
        if datetime.today() >= datetime_object:
            res2.append(r)

    if request.args.get('expired') == '1':
        url = 'https://notify-api.line.me/api/notify'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer '+linetoken
        }
        message = ['\n'+r['name']+' : '+r['amount']+' : '+r['expired'] for r in res2]
        print(message)
        data = {
            'message': message
        }
        x = requests.post(url=url, headers=headers, data=data)
    return render_template('expired.html', res=res2)

# @app.route('/search', methods=['DELETE'])
# def search():
#     response = fridge.find({'name': request.args.get('name')})
#     res = [r for r in response]
#     return render_template('search.html', res=res)

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)