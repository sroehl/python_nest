import pygal
import boto3
from NestDataPoint import NestDataPoint
from NestDataSet import NestDataSet
import time


def load_data(id, start_time=None, end_time=None):
    if start_time is None:
        start_time = round(time.time()) - (60*60*24*7)
    if end_time is None:
        end_time = round(time.time())
    data_set = NestDataSet()
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('HomeTempItems')
        #result = table.scan(FilterExpression=Attr('id').eq(id) & Attr('date').gt(start_time) & Attr('date').lt(end_time))
        result = table.scan()
        items = result['Items']
        for item in items:
            data_set.add_point(NestDataPoint(item['date'], float(item['temp']), float(item['target_temp']), float(item['humidity']), item['away'], item['fan'], item['mode'], item['state'], float(item['outside_temp'])))
        #print("dataset length: {}".format(len(data_set)))
    except Exception as ex:
        print("failure: {}".format(ex))
    return data_set


def make_line_chart(data_set, filename=None):
    config = pygal.Config()
    config.defs.append('''<linearGradient id="gradient-3" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#ffffff" />
        <stop offset="100%" stop-color="#0000ff " />
        </linearGradient>''')
    config.css.append('''inline:
      .color-2 {
        fill: url(#gradient-3    !important;
        stroke: url(#gradient-3) !important;
      }''')
    line_chart = pygal.DateTimeLine(x_label_rotation=35, truncate_label=-1,
                                    x_value_formatter=lambda dt: dt.strftime('%b %d %Y at %I:%M:%S %p'),
                                    range=(data_set.get_min_range()-2, data_set.get_max_range()+1),
                                    stroke_style={'width': 5},
                                    config=config)
    line_chart.add('Temp', data_set.get_temps(), show_dots=True)
    line_chart.add('Target Temp', data_set.get_target_temps(), show_dots=True)
    line_chart.add('Outside Temp', data_set.get_outside_temps(), show_dots=True)
    line_chart.add('State', data_set.get_states(), fill=True, show_dots=True)
    if filename is not None:
        line_chart.render_to_file(filename)
    else:
        return line_chart.render()

def create_graph():
    ds = load_data(0)
    make_line_chart(ds, filename='/tmp/weekly.svg')
    client = boto3.client('s3')
    with open('/tmp/weekly.svg', 'rb') as f:
        client.upload_fileobj(f, 'aws-website-housetemperaturetracker-w8nyd', 'weekly.svg')
