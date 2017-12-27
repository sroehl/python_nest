import datetime
import sqlite3
from NestDataPoint import NestDataPoint
import statistics
import numpy as np
from sql_to_plot import load_data
from dynamodb_load_data import load_data_dynamodb



def get_data_for_date(year, month, day, data_loader):
    start_epoch = datetime.datetime(year, month, day, 0, 0).timestamp()
    end_epoch = datetime.datetime(year, month, day, 23, 59).timestamp()
    return data_loader(start_time=start_epoch, end_time=end_epoch)

def sec_to_min(seconds):
   return round(seconds/60,2)

def remove_outliers(data_set):
    if len(data_set) < 2:
        return data_set
    x = []
    y = []
    for row in data_set:
        x.append(row[0])
        y.append(row[1])
    stdev = statistics.stdev(y)
    mean = statistics.mean(y)
    #print("stdev:{} mean:{}".format(np.std(y), mean))
    reject = 2 * stdev
    clean_set = []
    for row in data_set:
        if abs(row[1] - mean) < reject:
            clean_set.append(row)
    print("Removed {} records".format(len(data_set)-len(clean_set)))
    return clean_set

def get_stats_for_date(year, month, day, debug=False):
    if debug:
        print("Stats for {}/{}/{}".format(month, day, year))
    heat = 0
    cool = 0
    prev_heat_time = None
    prev_cool_time = None
    ds = get_data_for_date(year, month, day, load_data_dynamodb)
    for ndp in ds.points:
        time = int(ndp.time)
        if state == NestDataPoint.STATE_COOL and prev_cool_time is None:
            prev_cool_time = time
        elif state == NestDataPoint.STATE_HEAT and prev_heat_time is None:
            prev_heat_time = time
        elif state == NestDataPoint.STATE_OFF:
            if prev_heat_time is not None:
                heat += (time - prev_heat_time)
                prev_heat_time = None
            if prev_cool_time is not None:
                cool += (time - prev_cool_time)
                prev_cool_time = None
    if debug:
        print("Heat was on for {} minutes".format(sec_to_min(heat)))
        print("Cool was on for {} minutes".format(sec_to_min(cool)))
    return (sec_to_min(heat), sec_to_min(cool))

def get_leakage_heat_for_date(year, month, day, debug=False):
    if debug:
        print("Leakage for {}/{}/{}".format(year, month, day))
    prev_temp = None
    prev_time = None
    leakage_records = []
    ds = get_data_for_date(year, month, day, load_data_dynamodb)
    for ndp in ds.points: 
        if prev_temp is not None and prev_time is not None:
            if ndp.temp >= ndp.target_temp and (prev_temp - ndp.temp) == 1:
                leakage_time = ndp.time - prev_time
                difference = ndp.temp - ndp.outside_temp
                leakage_records.append([difference, sec_to_min(leakage_time)])
                prev_temp = ndp.temp
                prev_time = ndp.time
        else:
            prev_temp = ndp.temp
            prev_time = ndp.time
    return leakage_records

def get_warmup_time(year, month, day, debug=False):
    if debug:
        print("Warmup time for {}/{}/{}".format(year, month, day))
    prev_temp = None
    prev_time = None
    warmup_records = []
    ds = get_data_for_date(year, month, day, load_data_dynamodb)
    for ndp in ds.points:
        if prev_temp is not None and prev_time is not None:
            if debug:
                print("diff:{}".format(ndp.temp-prev_temp))
            if ndp.temp <= ndp.target_temp and (ndp.temp-prev_temp) == 1:
                warmup_time = ndp.time - prev_time
                difference = ndp.temp - ndp.outside_temp
                warmup_records.append([difference, sec_to_min(warmup_time)])
                prev_temp = ndp.temp
                prev_time = ndp.time
            if ndp.temp >= ndp.target_temp:
                prev_temp = ndp.temp
                prev_time = ndp.time
        else:
            prev_temp = ndp.temp
            prev_time = ndp.time
    return warmup_records


if __name__ == '__main__':
    year = 2017
    month = 12
    records = []
    for day in range(7,12):
    #    heat, cool = get_stats_for_date(year, month, day)
    #    print("{}/{}/{},{},{}".format(year,month,day,heat,cool))
        records += get_warmup_time(year,month,day)
    for rec in records:
        print(",".join(str(x) for x in rec))


