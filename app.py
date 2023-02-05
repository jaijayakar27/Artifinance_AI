from flask import Flask,render_template,jsonify,make_response,request
import numpy as np
import json
import pickle
from flask_cors import cross_origin
import bz2file
model = bz2file.BZ2File('model.pbz2','rb')
model = pickle.load(model)
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    json_ = request.json
    query = (json_)
    prediction = model.predict(query)
    return jsonify({'predictions':list(prediction)})
@app.route('/webhook',methods=['GET','POST'])
@cross_origin()
def webhook():
    req = request.json
    res = mlprediction(req)
    res.headers['Content-Type']='application/json'
    return res

def mlprediction(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    income = parameters.get("Income")
    age = parameters.get("Age") 
    exp = parameters.get("Experience")
    mar = parameters.get("Married")
    house = parameters.get("House")
    car = parameters.get("Car")
    Cexp = parameters.get("Cexp")
    Chouse = parameters.get("Chouse")
    if str.lower(mar) == 'yes' or str.lower(mar)=='y':
        mar = int(1)
    elif str.lower(mar) == 'no' or str.lower(mar)=='n':
        mar = int(0)
    else:
        return jsonify({
            "fulfillmentText": "Error please start again and enter the correct information"  
        })  
    if str.lower(house) == 'yes' or str.lower(house)=='y':
        house = int(1)
    elif str.lower(house) == 'no' or str.lower(house)=='n':
        house = int(0)
    else:
        return jsonify({
            "fulfillmentText": "Error please start again and enter the correct information"  
        })
    if str.lower(car) == 'yes' or str.lower(car)=='y':
        car = int(1)
    elif str.lower(car) == 'no' or str.lower(car)=='n':
        car = int(0)
    else:
        return jsonify({
            "fulfillmentText": "Error please start again and enter the correct information"  
        }) 
    try:
        int_features = [income,age,exp,mar,house,car,Cexp,Chouse]
        final_features = [np.array(int_features)]
    
    except ValueError:
        return jsonify({
            "fulfillmentText": "Incorrect information supplied"
        })
    intent = result.get("intent").get('displayName')

    if intent == "Default Welcome Intent - yes":
        prediction = model.predict(final_features)
        if(prediction==[0]):
            status = 'Congratulations you are eligible for a loan 😀'
        else:
            status = 'We are sorry you are not eligible for a loan at the moment'
        fulfillmentText= status
        return jsonify({"fulfillmentText":fulfillmentText})
    else:
        return jsonify({"fullfillmentText":"Error da"})

if __name__ == '__main__':
    app.run(debug=True)
