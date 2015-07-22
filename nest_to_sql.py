#!/usr/bin/env python

import nest
import ConfigParser
import sqlite3
import time

conn = sqlite3.connect('nest_data.db')
cur = conn.cursor()

config = ConfigParser.ConfigParser()
config.read("credentials.config")


username = config.get('credentials','username')
password = config.get('credentials','password')

#napi = nest.Nest(username, password)
#home = napi.structures[0]


def alreadyInserted(curr_time):
	cur.execute('select count(*) from data where time="%s"' % (curr_time))
	count = cur.fetchone()[0]
	if count > 0:
		return True
	else:
		return False

while 1:
	#print "running"
	try:
		napi = nest.Nest(username, password)
		home = napi.structures[0]
		curr_time = home.weather.current.datetime.strftime('%Y-%m-%d %H:%M:%S')
		temp = nest.utils.c_to_f(home.devices[0].temperature)
		outside_temp = nest.utils.c_to_f(home.weather.current.temperature)
		humidity = home.devices[0].humidity
		outside_humidity = home.weather.current.humidity
		if home.away == False:
			away = 0
		else:
			away = 1
		if home.devices[0].fan == False:
			fan = 0
		else:
			fan = 1
			
		if home.devices[0].mode == 'cool':
			mode = 0
		else:
			mode = 1
			
		#print 'insert into data values ("%s",%d,%d,%d,%d,%i,%i,%i)' % (curr_time,temp,outside_temp,humidity,outside_humidity,away,fan,mode)
		
		if not alreadyInserted(curr_time):
			cur.execute('insert into data values ("%s",%d,%d,%d,%d,%i,%i,%i)' % (curr_time,temp,outside_temp,humidity,outside_humidity,away,fan,mode))
			conn.commit()
		time.sleep(60)
	except:
		time.sleep(120)

