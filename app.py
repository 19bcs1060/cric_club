from flask import Flask, render_template, url_for,request
import requests
import pickle
import numpy as np

# Load the Random Forest CLassifier model
filename = 'first_innings_score-ridge-model.pkl'
regressor = pickle.load(open(filename, 'rb'))


app=Flask(__name__)

#decorator-runs before functions
@app.route('/')
def index():
    url = "https://serpapi.com/search.json?q=IPL+recent+matches&location=austin%2C+texas%2C+united+states&api_key=9a4a9b6c0e5b3d2ac34b5d423dfcadcfa6931d8b4f6e165692b15a7f1ecd545f"

    response = requests.request('GET', url).json()

    data_1= response['sports_results']['games'][0:3]


    url4= "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=51e2b4221012473d95ced266787f2494"
    response4= requests.request('GET', url4).json()
    case4={
        'article': response4['articles'][0:5]
    }
    return render_template("index.html", data_1=data_1, articles=case4)
@app.route('/predict')
def  predict():
	return render_template('predict.html')

@app.route('/result', methods=['POST'])
def result():
    temp_array = list()
    
    if request.method == 'POST':
        
        batting_team = request.form['batting-team']
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        bowling_team = request.form['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])
        
        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data)[0])
              
        return render_template('result.html', lower_limit = my_prediction-10, upper_limit = my_prediction+5)

if __name__=='__main__':
    app.run(debug=True)