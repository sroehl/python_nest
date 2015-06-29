#!/usr/bin/env python

import nest
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("credentials.config")


username = config.get('credentials','username')
password = config.get('credentials','password')

napi = nest.Nest(username, password)


print 'Away: %s' % napi.structures[0].away
print 'Temp: %0.1f' % nest.utils.c_to_f(napi.structures[0].devices[0].temperature)
