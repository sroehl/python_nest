import pygal
import sqlite3
from NestDataPoint import NestDataPoint
from NestDataSet import NestDataSet
import time


def load_data(start_time=None, end_time=None):
    if start_time is None:
        start_time = round(time.time()) - (60*60*24*7)
    if end_time is None:
        end_time = round(time.time())
    data_set = NestDataSet()
    conn = sqlite3.connect('nest_data.db')
    cur = conn.cursor()
    stmt = 'select * from data where time >= ? and time <= ? order by time'
    for row in cur.execute(stmt, (start_time, end_time)):
        row_time, temp, target_temp, humidity, away, fan, mode, state, outside_temp = row
        data_set.add_point(NestDataPoint(row_time, temp, target_temp, humidity, away, fan, mode, state, outside_temp))

    print("dataset length: {}".format(len(data_set)))
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

if __name__ == '__main__':
    ds = load_data()
    make_line_chart(ds, filename='weekly.svg')
