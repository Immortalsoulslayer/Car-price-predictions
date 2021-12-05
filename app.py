from flask import Flask,render_template,request
import pickle
import requests
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScalar
app=Flask(__name__)
model=pickle.load(open('random_forest_regression_model.pkl','rb'))
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')
 
    
Standard_to = StandardScalar()
@app.route("/predict",methods=['POST'])
def predict():
    fuel_Diesel=0
    fuel_LPG=0
    owner_Fourth=0
    owner_Second=0
    owner_Test_Drive_Car=0
    owner_Third_Owner=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        seats = int(request.form['seats'])
        km_driven=int(request.form['km_driven'])
        owner=int(request.form['owner'])
        if(owner==0):
            owner_Fourth=0
            owner_Second=0
            owner_Test_Drive_Car=0
            owner_Third_Owner=0
            
        elif(owner==1):
            owner_Fourth=0
            owner_Second=1
            owner_Test_Drive_Car=0
            owner_Third_Owner=0
        
        elif(owner==2):
            owner_Fourth=0
            owner_Second=0
            owner_Test_Drive_Car=0
            owner_Third_Owner=1
        else:
            owner_Fourth=1
            owner_Second=0
            owner_Test_Drive_Car=0
            owner_Third_Owner=0
            
        
        fuel_Petrol=request.form['fuel_Petrol']
        if(fuel_Petrol=='Petrol'):
                fuel_Petrol=1
                fuel_Diesel=0
                fuel_LPG=0
        elif(fuel_Petrol=='Diesel'):
            fuel_Petrol=0
            fuel_Diesel=1
            fuel_LPG=0
        else:
            fuel_Diesel=0
            fuel_Petrol=0
            fuel_LPG=1

        no_years=2021-Year
        transmission_Manual=request.form['transmission_Manual']
        if(transmission_Manual=='Mannual'):
            transmission_Manual=1
        else:
            transmission_Manual=0
        prediction=model.predict([[km_driven,seats,no_years,fuel_Diesel,fuel_LPG,fuel_Petrol,transmission_Manual,owner_Fourth,owner_Second,owner_Test_Drive_Car,owner_Third_Owner]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)    