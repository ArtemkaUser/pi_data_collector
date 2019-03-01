#!/usr/bin/env python3
from flask import Flask, request, render_template
from grafana_api import *
from datetime import datetime
from influxdb_handler import *
from datetime import timedelta

influx_handler = InfluxClient(
    'localhost',
    8086,
    'root',
    'root',
    'data'
)

app = Flask(__name__)
uid = 'rzlhlzrik'
link_server = "http://localhost:3000/d/"
link_station = "/stantsiia-1?"
link_refresh = "refresh=1s"
link_end = "&panelId=2&fullscreen&orgId=1&kiosk"
link_from = "&from="
link_to = "&to="
link = link_server + uid + link_station


def get_data_n_time():
    return [
        datetime.strftime(datetime.now(), "%Y-%m-%d"),
        "00:00",
        datetime.strftime(datetime.now(), "%Y-%m-%d"),
        datetime.strftime(datetime.now(), "%H:%M")
    ]


@app.route('/')
def root():
    from_d, from_t, to_d, to_t = get_data_n_time()
    json = get_json(uid)
    name = get_name_panel(json)
    return render_template('index.html', graph=name, link=link + link_refresh + link_from + "now-15m" + link_end,
                           from_date=from_d, from_time=from_t, to_date=to_d, to_time=to_t, operation_t='--:--:--')


@app.route('/', methods=['POST'])
def form_post():
    json = get_json(uid)
    from_date, from_time, to_date, to_time = get_data_n_time()
    try:
        station_text = request.form['station_name']
        change_name(json, station_text)
        push_json(uid, json)
        name = get_name_panel(json)
        return render_template('index.html', graph=name, link=link + link_refresh + link_from + "now-15m" + link_end,
                               from_date=from_date, from_time=from_time, to_date=to_date, to_time=to_time,
                               operation_t='--:--:--')
    except:
        pass
    try:
        from_date = request.form['from_date']
        from_time = request.form['from_time']
        to_date = request.form['to_date']
        to_time = request.form['to_time']

        fd = from_date.split('-')
        ft = from_time.split(':')
        td = to_date.split('-')
        tt = to_time.split(':')

        s_from = datetime(int(fd[0]), int(fd[1]), int(fd[2]), int(ft[0]), int(ft[1]), 0)
        s_to = datetime(int(td[0]), int(td[1]), int(td[2]), int(tt[0]), int(tt[1]), 0)
        ts_from = (s_from - datetime(1970, 1, 1)).total_seconds()
        ts_to = (s_to - datetime(1970, 1, 1)).total_seconds()
        link_result = link + link_from + str(int(ts_from)*1_000-10_800_000)
        link_result += link_to + str(int(ts_to)*1000-10_800_000) + link_end

        name = get_name_panel(json)

        query_oper_time = "select count(value) from data where time > '" + str(s_from).split(' ')[0] + "T"
        query_oper_time += str(s_from).split(' ')[1] + "Z'" + " and time < '" + str(s_to).split(' ')[0] + "T"
        query_oper_time += str(s_to).split(' ')[1] + "Z'"
        operation_time = int(influx_handler.get_value(query_oper_time))
        operation_time = timedelta(seconds=operation_time)

        return render_template('index.html', graph=name, link=link_result,
                               from_date=from_date, from_time=from_time,
                               to_date=to_date, to_time=to_time,
                               operation_t=operation_time)
    except:
        pass
    try:
        min_value = request.form['min']
        max_value = request.form['max']
        json = get_json(uid)
        if min != "":
            json.get('dashboard').get('panels')[0].get('targets')[0].get('tags')[0].update({'value': min_value})
        else:
            json.get('dashboard').get('panels')[0].get('targets')[0].get('tags')[0].update({'value': '0'})
        if max != "":
            json.get('dashboard').get('panels')[0].get('targets')[0].get('tags')[1].update({'value': max_value})
        else:
            json.get('dashboard').get('panels')[0].get('targets')[0].get('tags')[1].update({'value': "500"})
        push_json(uid, json)
    except:
        pass
    name = get_name_panel(json)
    return render_template('index.html', graph=name, link=link + link_refresh + link_from + "now-15m" + link_end,
                           from_date=from_date, from_time=from_time,
                           to_date=to_date, to_time=to_time,
                           operation_t='--:--:--')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
