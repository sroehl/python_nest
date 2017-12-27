from flask import Flask, make_response, request
from sql_to_plot import *
from dynamodb_load_data import load_data_dynamodb
from stats import get_leakage_heat_for_date, remove_outliers, get_warmup_time
import time
import os

app = Flask(__name__)

last_created = {}

@app.route('/')
def chart():
    chart_path = os.path.join('resources', 'main.svg')
    if 'main' not in last_created or (last_created['main'] + (5 *60)) > time.time():
        days = int(request.args.get('days', 7))
        data_set = load_data_dynamodb(days=days)
        make_line_chart(data_set, chart_path)
        last_created['main'] = time.time()
    response = make_response(open(chart_path).read())
    response.content_type = 'image/svg+xml'
    return response

@app.route('/heat_leakage')
def heat_leakage_chart():
    chart_path = os.path.join('resources', 'heat_leakage.svg')
    if 'heat_leakage' not in last_created or (last_created['heat_leakage'] + (5 * 60)) > time.time():
        year = 2017
        month = 12
        data_set = []
        for day in range(1,31):
            data_set += get_leakage_heat_for_date(year, month, day)
        data_set = remove_outliers(data_set)
        svg = make_plain_line_chart(data_set, 'Heat Leakage',  'Difference (F)', 'Time (min)', chart_path)
        last_created['heat_leakage'] = time.time()
    response = make_response(open(chart_path).read())
    response.content_type = 'image/svg+xml'
    return response

@app.route('/warmup')
def warmup_chart():
    chart_path = os.path.join('resources', 'warmup.svg')
    if 'warmup' not in last_created or (last_created['warmup'] + (5 * 60)) > time.time():
        year = 2017
        month = 12
        data_set = []
        for day in range(1,31):
            data_set += get_warmup_time(year, month, day)
        data_set = remove_outliers(data_set)
        svg = make_plain_line_chart(data_set, 'Warmup', 'Difference (F)', 'Time (min)', chart_path)
        last_created['warmup'] = time.time()
    response = make_response(open(chart_path).read())
    response.content_type = 'image/svg+xml'
    return response


if __name__=='__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
