#!/usr/bin/python

import threading
import random
import sqlite3
import time
import datetime


current_milli_time = lambda: int(round(time.time() * 1000))
current_date = lambda: str(datetime.date.today().strftime("%d.%m.%Y"))

sqlite_file = 'temp_db.sqlite'
table1 = 'temp_tab'
col1 = 'number'
col2 = 'time'
col3 = 'temperature'
col4 = 'date'

class TempMonitor(object):

    def __init__(self):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        try:
            c.execute("DROP TABLE IF EXISTS {tn}" \
                .format(tn = table1))
            c.execute("CREATE TABLE {tn} ({n1} {v1} PRIMARY KEY AUTOINCREMENT, {n2} {v2}, {n3} {v3}, {n4} {v4})" \
                .format(tn = table1, n1 = col1, v1 = 'INTEGER', \
                n2 = col2, v2 = 'INTEGER', n3 = col3, v3 = 'INTEGER', n4 = col4, v4 = 'TEXT'))


        except sqlite3.IntegrityError:
            print('ERROR: db exists')

        conn.commit()
        conn.close()

    def every_30_s(self):
        temp = random.randrange(20, 30)
        threading.Timer(30.0, self.every_30_s).start()
        print "Temperature: " + str(temp)
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        print current_date()
        date = current_date()
        c.execute("INSERT INTO {tn} ({it}, {t}, {dt}) VALUES ({vi}, {vt}, '{vdt}')" \
            .format(tn = table1, it = col2, t = col3, dt = col4, vi = current_milli_time(), vt = temp,  vdt = date))

        conn.commit()
        conn.close()

if __name__=='__main__':
    tempMonitor = TempMonitor()
    tempMonitor.every_30_s()
