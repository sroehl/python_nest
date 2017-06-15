

class NestDataPoint:
    FAN_OFF = 0
    FAN_ON = 1

    AWAY = 0
    HOME = 1

    MODE_OFF = 0
    MODE_HEAT = 1
    MODE_COOL = 2
    MODE_ECO = 3

    STATE_OFF = 0
    STATE_HEAT = 1
    STATE_COOL = 2

    def insert_to_sql(self, cursor):
        cursor.execute('insert into data values (?, ?, ?, ?, ?, ?, ?, ?)', (
            self.time, self.temp, self.target_temp, self.humidity, self.away, self.fan, self.mode, self.state))

    def __init__(self, time, temp, target_temp, humidity, away, fan, mode, state):
        self.time = time
        self.temp = temp
        self.target_temp = target_temp
        self.humidity = humidity
        self.away = away
        self.fan = fan
        self.mode = mode
        self.state = state
