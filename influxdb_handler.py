from influxdb import InfluxDBClient
import random
import time
query = 'select value from data;'

class InfluxClient:
    def __init__(self, ip, port, user_name, password, db_name):
        self.query = query
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.client = InfluxDBClient(self.ip, self.port, self.user_name, self.password, self.db_name)
        self.client.create_database(self.db_name)


    def write(self, value):
        json_body = [
            {
                "measurement": self.db_name,
                "fields": {
                    "value": value
                }
            }
        ]
        self.client.write_points(json_body)

    def drop_dp(self):
        self.client.drop_database(self.db_name)

    def show_data(self, query):
        result = self.client.query(query)
        return result

    def get_value(self, query):
        result = self.client.query(query)
        return int(list(result.get_points())[0].get('count'))
    # def snmp_get_data(self):
    #     data = snmp_get('1.3.6.1.4.1.40418.2.2.4.2', hostname='192.168.15.20', community='public', version=1)
    #     return str(data).split("'")[1]

if __name__ == '__main__':
    influxdb_handler = InfluxClient(
        'localhost',
        8086,
        'root',
        'root',
        'data'
    )
    while True:
         influxdb_handler.write(random.randrange(90,100))
         time.sleep(1)
