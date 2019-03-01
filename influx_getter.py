import influxdb
from influxdb_handler import *

ip = ""

influx_input = InfluxClient(
    ip,
    8086,
    'root',
    'root',
    'data'
)

influx_output = InfluxClient(
    'localhost',
    8086,
    'root',
    'root',
    'data'
)

while True:
    try:
        answer = list(influx_input.client.query("select last(value) from data where time > now()-1s").get_points())[0].get("last")
        influx_output.write(answer)
    except:
        influx_output.write(0)
    time.sleep(1)