#!/usr/bin/env python

import nest

username = 'sprzeo@gmail.com'
password = #change to password

napi = nest.Nest(username, password)

for structure in napi.structures:
    print 'Structure %s' % structure.name
    print '    Away: %s' % structure.away
    print '    Devices:'

    for device in structure.devices:
        print 'Device: %s' % device.name
        print 'Temp: %0.1f' % nest.utils.c_to_f(device.temperature)