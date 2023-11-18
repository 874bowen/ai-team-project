import flask
from flask import Flask
from datetime import date
import pandas as pd
import pickle

from flask import redirect, url_for, render_template, flash, request, send_from_directory, jsonify

app = Flask(__name__, template_folder='templates')

with open(f'model/expenditure2.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def main():  # put application's code here
    if flask.request.method == 'GET':
        return flask.render_template('main.html')
    if flask.request.method == 'POST':
        temperature = flask.request.form['temperature']
        rainfall = flask.request.form['humidity']
        month = flask.request.form['month-today']
        place = flask.request.form['select_place']
        age = flask.request.form['age']
        income = flask.request.form['income']
        duration = flask.request.form['duration']
        gender = flask.request.form['select_gender']
        no_of_people = flask.request.form['no_of_people']
        accommodation = flask.request.form['select_accommodation']
        months = [0] * 11
        accommodations = [0] * 8

        year = date.today().year

        if accommodation == "Airbnb":
            accommodations[0] = 1
        elif accommodation == "Campsite":
            accommodations[1] = 1
        elif accommodation == "Guest House":
            accommodations[2] = 1
        elif accommodation == "Hostel":
            accommodations[3] = 1
        elif accommodation == "Hotel":
            accommodations[4] = 1
        elif accommodation == "Motel":
            accommodations[5] = 1
        elif accommodation == "Resort":
            accommodations[6] = 1
        elif month == 8:
            months[10] = 1
        elif month == 9:
            months[9] = 1
        elif month == 10:
            months[8] = 1

        if month == 1:
            months[3] = 1
        elif month == 2:
            months[6] = 1
        elif month == 3:
            months[0] = 1
        elif month == 4:
            months[7] = 1
        elif month == 5:
            months[5] = 1
        elif month == 6:
            months[4] = 1
        elif month == 7:
            months[1] = 1
        elif month == 8:
            months[10] = 1
        elif month == 9:
            months[9] = 1
        elif month == 10:
            months[8] = 1
        elif month == 11:
            months[2] = 1
        else:
            months = months

        input_variables = pd.DataFrame(
            [[year, rainfall, temperature, age, income, duration, no_of_people, *months, gender, *accommodations]],
            columns=[
                'Year',
                'Rainfall - (MM)',
                'Temperature - (Celsius)',
                'Age',
                'Income (USD)',
                'Duration of Stay',
                'Num. of People',
                'Apr Average',
                'Aug Average',
                'Dec Average',
                'Feb Average',
                'Jul Average',
                'Jun Average',
                'Mar Average',
                'May Average',
                'Nov Average',
                'Oct Average',
                'Sep Average',
                'Male',
                'Airbnb',
                'Campsite',
                'Guest House',
                'Hostel',
                'Hotel',
                'Motel',
                'Resort',
                'Villa',
            ],
            dtype=float)
        prediction = model.predict(input_variables)[0]
        return flask.render_template('main.html',
                                     original_input={'Temperature': temperature,
                                                     'Humidity': rainfall},
                                     result=round(prediction, 2),
                                     place=place
                                     )


if __name__ == '__main__':
    app.run()
