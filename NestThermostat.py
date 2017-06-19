from nest_helpers import *
from NestDataPoint import NestDataPoint
import time


class NestThermostat:
    UPDATE_INTERVAL = 120

    def get_inside_temp(self, use_c=False):
        key = 'ambient_temperature_c' if use_c else 'ambient_temperature_f'
        return self.get_thermo_value(key)

    def get_target_temp(self, use_c=False):
        key = 'target_temperature_c' if use_c else 'target_temperature_f'
        return self.get_thermo_value(key)

    def get_humidity(self):
        return self.get_thermo_value('humidity')

    def get_state(self):
        raw_value = self.get_thermo_value('hvac_state')
        if raw_value == 'off':
            return NestDataPoint.STATE_OFF
        elif raw_value == 'heating':
            return NestDataPoint.STATE_HEAT
        elif raw_value == 'cooling':
            return NestDataPoint.STATE_COOL

    def get_mode(self):
        raw_value = self.get_thermo_value('hvac_mode')
        if raw_value == 'off':
            return NestDataPoint.MODE_OFF
        elif raw_value == 'heat':
            return NestDataPoint.MODE_HEAT
        elif raw_value == 'cool':
            return NestDataPoint.MODE_COOL
        elif raw_value == 'eco':
            return NestDataPoint.MODE_ECO

    def get_fan_status(self):
        raw_value = self.get_thermo_value('fan_timer_active')
        if raw_value:
            return NestDataPoint.FAN_ON
        else:
            return NestDataPoint.FAN_OFF

    def get_away_status(self):
        structure_id = self.get_thermo_value('structure_id')
        raw_value = self.data['structures'][structure_id]['away']
        if raw_value == 'away':
            return NestDataPoint.AWAY
        elif raw_value == 'home':
            return NestDataPoint.HOME

    def get_thermo_value(self, key):
        thermo_data = self.get_thermostat_data()
        if key in thermo_data:
            return thermo_data[key]
        else:
            raise KeyError("'{}' not found in thermostat data".format(key))

    def get_thermostat_data(self, id=None):
        try:
            if id is None:
                id = list(self.data['devices']['thermostats'].keys())[0]
            return self.data['devices']['thermostats'][id]
        except:
            return None

    def update_data(self):
        self.data = read_data(self.token)
        self.last_ret_time = round(time.time())

    def get_outside_temp(self):
        weather_data = get_weather_data(self.zipcode)
        temp = weather_data['main']['temp']
        return round(temp) # Rounding because data from Nest is less accurate

    def get_datapoint(self):
        self.update_data()
        dp = NestDataPoint(self.last_ret_time, self.get_inside_temp(), self.get_target_temp(), self.get_humidity(),
                           self.get_away_status(), self.get_fan_status(), self.get_mode(), self.get_state(),
                           self.get_outside_temp())
        return dp

    def __init__(self, zipcode, token=None):
        if token is None:
            self.token = get_token()
        else:
            self.token = token
        if self.token is None:
            raise Exception("Token is not defined")
        self.last_ret_time = 0
        self.data = {}
        self.update_data()
        self.zipcode = zipcode
