import pygal
import sqlite3
from NestDataPoint import NestDataPoint
from NestDataSet import NestDataSet



def load_data():
    data_set = NestDataSet()
    conn = sqlite3.connect('nest_data.db')
    cur = conn.cursor()
    prev_temp = 0
    prev_target_temp = 0
    prev_state = 0
    prev_outside_temp = 0
    for row in cur.execute('select * from data order by time'):
        time, temp, target_temp, humidity, away, fan, mode, state, outside_temp = row
        #  This changes the graph too much
        #if temp != prev_temp or target_temp != prev_target_temp or state != prev_state or outside_temp != prev_outside_temp:
        data_set.add_point(NestDataPoint(time, temp, target_temp, humidity, away, fan, mode, state, outside_temp))
        prev_temp = temp
        prev_target_temp = target_temp
        prev_state = state
        prev_outside_temp = outside_temp
    print("dataset length: {}".format(len(data_set)))
    return data_set

def make_line_chart(data_set, file=False):
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
    if file:
        line_chart.render_to_file('chart.svg')
    else:
        return line_chart.render()

if __name__ == '__main__':
    ds = load_data()
    make_line_chart(ds, file=True)
