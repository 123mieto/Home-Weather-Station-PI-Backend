#!/usr/bin/python

import threading, random, sqlite3, time, datetime, requests
from  DBAccessor import DBAccessor
#--------------------------- Local lambdas ----------------------------
current_milli_time = lambda: int(round(time.time() * 1000))
current_date = lambda: str(datetime.date.today().strftime("%d.%m.%Y"))
#------------------------------------------------------------------------

#--------------------------- Local defines ------------------------------
ENDPOINT_ESP8266 = "http://192.168.0.80/"
LIGHT_MEAS_NUM = 5
LIGHT_MEAS_T_INTERVAL = 10 #minutes
MINUTE = 60 #seconds
#------------------------------------------------------------------------

#--------------------------- Public variables----------------------------
#------------------------------------------------------------------------

#--------------------------- Global variables----------------------------
global access
#------------------------------------------------------------------------

#--------------------------- Private functions---------------------------
def __get_light():
    lightLAvg = 0
    for i in xrange(LIGHT_MEAS_NUM):
        lightResp = requests.get(ENDPOINT_ESP8266 + "light_lvl")
        print lightResp.status_code
        if lightResp.status_code == 200:
            lightLAvg += int(lightResp.content)
        else:
            return str(lightLAvg / i)
        time.sleep(1.0)

    return str(lightLAvg / LIGHT_MEAS_NUM)
#----------------------------------------------------------------------

#--------------------------- Public functions----------------------------
def cyclic_meas():
    global access
    #TODO
    temp = random.randrange(20, 30)

    threading.Timer(MINUTE * LIGHT_MEAS_T_INTERVAL, cyclic_meas).start()
    #TODO\
    print "Temperature: " + str(temp)
    print current_date()
    date = current_date()
    access.insert_temp_meas(current_milli_time(), temp, date)
    light = __get_light()
    if light != None:
        access.insert_light_meas(current_milli_time(), light, date)
#----------------------------------------------------------------------

if __name__=='__main__':
    global access
    access = DBAccessor()
    cyclic_meas()
