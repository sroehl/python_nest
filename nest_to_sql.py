from NestThermostat import NestThermostat
import configparser
import sqlite3
import time
import sys

conn = sqlite3.connect('nest_data.db')
cur = conn.cursor()

nest = NestThermostat()


def already_inserted(curr_time):
    cur.execute('select count(*) from data where time="%s"' % (curr_time))
    count = cur.fetchone()[0]
    if count > 0:
        return True
    else:
        return False

while 1:
    print("running")
    try:
        print("Getting datapoint")
        dp = nest.get_datapoint()
        dp.insert_to_sql(cur)
        conn.commit()
        time.sleep(10)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        time.sleep(120)
