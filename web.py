from flask import Flask, make_response
from sql_to_plot import *

app = Flask(__name__)

@app.route('/')
def chart():
    data_set = load_data()
    svg = make_line_chart(data_set)
    response = make_response(svg)
    response.content_type = 'image/svg+xml'
    return response

if __name__=='__main__':
    app.run(host='0.0.0.0', port=7000)
