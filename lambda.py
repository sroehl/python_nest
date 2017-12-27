import boto3
import time
from NestThermostat import NestThermostat
from dynamo_to_plot import create_graph
import traceback
import sys
import os

ZIP_CODE = '53511'

nest = NestThermostat(ZIP_CODE, lambda_id=0)

def insert_datapoint(table, dp):
    try:
        resp = table.put_item(TableName='HomeTempItems', Item = {'id': 0, 'date': dp.time, 'temp': dp.temp, 'target_temp': dp.target_temp, 'humidity': dp.humidity, 'away': dp.away, 'fan': dp.fan, 'mode': dp.mode, 'state': dp.state, 'outside_temp': dp.outside_temp}) 
        if 'ResponseMetadata' in resp:
            if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True 
    except Exception as ex:
        print("failed: {}".format(ex))
    return False

def lambda_handler(event, context):
    os.environ['TZ'] = 'US/Central'
    time.tzset()
    status = 0
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HomeTempItems')
    try:
        dp = nest.get_datapoint()
        if not insert_datapoint(table, dp):
            status = -1
        create_graph()
    except Exception as ex:
        print(traceback.format_exception(None, ex, ex.__traceback__), file=sys.stderr, flush=True)
        return -1
    return status

    

