from NestDataPoint import NestDataPoint
from NestDataSet import NestDataSet
import time
import math
import boto3
from boto3.dynamodb.conditions import Key, Attr


def load_data_dynamodb(start_time=None, end_time=None, days=1):
    if start_time is None:
        start_time = round(time.time()) - (60*60*24*days)
    else:
        start_time = int(start_time)
    if end_time is None:
        end_time = round(time.time())
    else:
        end_time = int(end_time)
    data_set = NestDataSet()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HomeTempItems2')
    response = table.scan(
        FilterExpression=Key("date").between(start_time, end_time)
    )
    items = response['Items']
    for item in items:
        ndp = data_set.add_point(NestDataPoint(item['date'], float(item['temp']), float(item['target_temp']), float(item['humidity']), item['away'], item['fan'], item['mode'], item['state'], float(item['outside_temp'])))
    print("dataset length: {}".format(len(data_set)))
    data_set.sort()
    return data_set

if __name__ == '__main__':
    ds = load_data_dynamodb()
    ds.sort()
    for ndp in ds.points:
        print(ndp.time)
