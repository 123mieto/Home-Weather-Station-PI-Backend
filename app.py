#!/usr/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, make_response, request, url_for

import time
import sys
import sqlite3
import logging
import json
import datetime
logging.basicConfig(filename='api.log',level=logging.DEBUG)


from flask_httpauth import HTTPBasicAuth

NUMBER = 0
TIMESTAMP = 1
TEMPERATURE = 2
DATE = 3



auth = HTTPBasicAuth()
app = Flask(__name__)

readings = [
    {
        'number': 1,
        'time': 10,
        'temperature': 20,
        'date':"10.10.10"
    }
]

days = [
    {
        'number':1,
        'date':"10.10.16",
        'temperatures': [20,21,23],
        'times':[89999999,89999999,87877878]
    }
]

sqlite_file = '../../pi/Temperature/temp_db.sqlite'


def __get_readings(start_num = 0, len = 100):
    print("Provided readings", file=sys.stderr)
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    try:
       if start_num < 0:
           start_num = 0
       if len <= 0:
           len = 1
       if start_num == 0 and len == 100:
           c.execute("SELECT * FROM {tn};" \
               .format(tn = 'temp_tab'))
       else:
           c.execute("SELECT * FROM {tn} WHERE {cn} >= {c1} AND {cn} < {c2};"\
               .format(tn = 'temp_tab', cn = 'no', c1 = start_num, c2 = start_num + len))
       results = c.fetchmany(len)
       if results is not None:
           result = [{'number': result[NUMBER], 'time': result[TIMESTAMP], 'temperature': result[TEMPERATURE], 'date': result[DATE]} for result in results[:len]]
       #close connection to db
       conn.commit()
       conn.close()

       return result
    except sqlite3.IntegrityError:
        print('ERROR: db exists')

#for now it always gets last 10 days
def __get_days():
    print("Provided days", file=sys.stderr)
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    daysData = []

    try:
        for i in range(10):
            tTemps = []
            tTimes = []
            date = (datetime.date.today() - datetime.timedelta(days = i)).strftime("%d.%m.%Y");
            c.execute("SELECT {q1}, {q2} FROM {tn} WHERE {cd} = '{vd}';" \
                .format(q1 = 'time', q2 = 'temperature',tn = 'temp_tab', cd = 'date', vd = date))
            results = c.fetchall()
            if results is not None:
                tTemps = [result[1] for result in results]
                tTimes = [result[0] for result in results]
            daysData.append({'number': i + 1, 'date': date, 'temperatures': tTemps, 'times': tTimes})

            #close connection to db
        conn.commit()
        conn.close()

        return daysData
    except sqlite3.IntegrityError:
        print('ERROR: db exists')

def __switch_led(state = 1):
    #TODO: wykonaj zmiane koloru ledki
    #TODO: stan ledki powinien byc globalny dla kazdej z podlaczonych led
    return state

def __led_status():
    print("Led status", file= sys.stderr)
    return 1

#TODO:
def __print_conn_hw():
    return 1

#TODO:
def __add_new_device(device):
    return 1
## AUTH STUFF ###

@auth.get_password
def get_password(username):
    if username == 'username':
        return 'password'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


## Function to add URI to each requests
def make_public_reading(reading):
    new_reading = {}
    for field in reading:
        if field == 'id':
            new_reading['uri'] = url_for('get_reading', reading_no=reading['id'], _external=True)
        else:
            new_reading[field] = reading[field]
    return new_reading


## 404 handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


## Routes
## /temperature/api/v1/readings  GET ALL
@app.route('/api/v1/temperature/readings', methods=['GET'])
#@auth.login_required
def get_readings():
    return jsonify({'readings': __get_readings()})

## /temperature/api/v1/readings  GET ONE
@app.route('/api/v1/temperature/readings/<int:reading_no>', methods=['GET'])
def get_reading(reading_no):
    reading = [reading for reading in __get_readings() if reading['number'] == reading_no]

    if len(reading) == 0:
        abort(404)
    return jsonify({'reading': reading[0]})

## /temperature/api/v1/days  GET ALL
@app.route('/api/v1/temperature/days', methods=['GET'])
#@auth.login_required
def get_days():
    return jsonify({'days': __get_days()})

## /temperature/api/v1/days  GET ONE
@app.route('/api/v1/temperature/days/<int:day_no>', methods=['GET'])
def get_day(day_no):
    days = __get_days()

    if len(days) == 0:
        abort(404)
    return jsonify({'day': days[day_no - 1]})

## /controller/api/v1/connected-hardware
@app.route('/api/v1/controller/connected-hardware', methods=['GET','POST'])
def hardware():
    if request.method == 'POST':
        # ex. controller/api/v1/connected-hardware?device=tempsensor
        device = request.args.get('device',type=str)
        status = __add_new_device(device)
        return jsonify({'status':status})
    else:
        return jsonify({'status':__print_conn_hw()})

@app.route('/api/v1/controller/leds', methods=['GET','POST'])
def leds():
    if request.method == 'POST':
        #return status of led switch_led
        #controller/api/v1/led?number=1&state=1
        number = request.args.get('number',type=int)
        state = request.args.get('state',type=int)
        if (state is None) or (number is None):
            print("State or number cannot be None: ", state, number,  file= sys.stderr)
            print ("Request url: ", request.url, file = sys.stderr)
            abort(404)
        if (state < 0) or (state > 1):
            print("State cannot be more than 1. State: ", state, file= sys.stderr)
            print ("Request url: ", request.url, file = sys.stderr)
            abort(404)
        if number == 1:
            print ("Request url: ", request.url, file = sys.stderr)
            return jsonify({'status': __switch_led(state)})
            print ("Request url: ", request.url, file = sys.stderr)
        else:
            abort(404)
    else:
        return jsonify({'status': __led_status()})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
