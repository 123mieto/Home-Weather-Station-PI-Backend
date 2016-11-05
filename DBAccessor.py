#!/usr/bin/python
from LogData import LogData
import threading
import random
import sqlite3
import time
import datetime


current_milli_time = lambda: int(round(time.time() * 1000))
current_date = lambda: str(datetime.date.today().strftime("%d.%m.%Y"))

sqlite_file = 'temp_db.sqlite'

table1 ='temp_tab'
col1 = 't_id'
col2 = 'time'
col3 = 'temperature'
col4 = 'date'

table2 = 'log_tab'
col2_1 = 'id'
col2_2 = 'start_time' #millis
col2_3 = 'stop_time'  #millis
col2_4 = 'connector_ip'

table3 = 'light_tab'
col3_1 = 'l_id'
col3_2 = 'time'
col3_3 = 'light'
col3_4 = 'date'

class DBAccessor(object):

    def __init__(self):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        try:
            c.execute("DROP TABLE IF EXISTS {tn1}" \
                .format(tn1 = table1))
            c.execute("DROP TABLE IF EXISTS {tn2}" \
                .format(tn2 = table2))
            c.execute("DROP TABLE IF EXISTS {tn3}"\
                .format(tn3 = table3))
            c.execute("CREATE TABLE {tn} ({n1} {v1} PRIMARY KEY AUTOINCREMENT, {n2} {v2}, {n3} {v3}, {n4} {v4})" \
                .format(tn = table1, n1 = col1, v1 = 'INTEGER', \
                n2 = col2, v2 = 'INTEGER', n3 = col3, v3 = 'INTEGER', n4 = col4, v4 = 'TEXT'))
            c.execute("CREATE TABLE {tn} ({n1} {v1} PRIMARY KEY AUTOINCREMENT, {n2} {v2}, {n3} {v3}, {n4} {v4})" \
                .format(tn = table2, n1 = col2_1, v1 = 'INTEGER', \
                n2 = col2_2, v2 = 'INTEGER', n3 = col2_3, v3 = 'INTEGER', n4 = col2_4, v4 = 'TEXT'))
            c.execute("CREATE TABLE {tn} ({n1} {v1} PRIMARY KEY AUTOINCREMENT, {n2} {v2}, {n3} {v3}, {n4} {v4})" \
                .format(tn = table3, n1 = col3_1, v1 = 'INTEGER', \
                n2 = col3_2, v2 = 'INTEGER', n3 = col3_3, v3 = 'INTEGER', n4 = col3_4, v4 = 'TEXT'))

        except sqlite3.IntegrityError:
            print('ERROR: db exists')

        conn.commit()
        conn.close()


    def insert_temp_meas(self, time, temp, date):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute("INSERT INTO {tn} ({it}, {t}, {dt}) VALUES ({vi}, {vt}, '{vdt}')" \
            .format(tn = table1, it = col2, t = col3, dt = col4, vi = time, vt = temp,  vdt = date))

        conn.commit()
        conn.close()

    def insert_light_meas(self, time, light, date):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute("INSERT INTO {tn} ({it}, {t}, {dt}) VALUES ({vi}, {vl}, '{vdt}')" \
            .format(tn = table3, it = col3_2, t = col3_3, dt = col3_4, vi = time, vl = light,  vdt = date))

        conn.commit()
        conn.close()

    #TODO: to powinno byc dopracowane bo logData jest nie sprawdzone
    def insert_log(self, logData):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute("INSERT INTO {tn} ({it}, {t}, {dt}) VALUES ({vi}, {vt}, '{vdt}')" \
            .format(tn = table2, it = col2_2, t = col2_3, dt = col2_4, vi = logData.get_start_time(), vt = logData.get_stop_time(),  vdt = logData.get_ip()))

        conn.commit()
        conn.close()
