import asyncio
import os
import logging as log
from snmp_handler import snmp_get_data
from influxdb_handler import InfluxClient
from const import *

class DataService:
    writing = False
    retrieving = False

    def __init__(self, out_file):
        self.queue = asyncio.Queue()
        self.out_file = out_file
    async def __retrieve_value(self) -> int:
        while True:
            try:
                yield snmp_get_data()
            except Exception as e:
                raise e

    async def start(self):
        await self.__start_data_retrieving()
        await self.__start_data_writing()

    async def get_file_data(self):
        data = None
        with open(self.out_file, 'r') as f:
            data = f.readlines()
        return data

    async def __start_data_retrieving(self):
        self.retrieving = True
        await self.queue.put(self.__retrieve_value())
        await asyncio.sleep(1)

    async def __start_data_writing(self):
        self.writing = True
        with open(self.out_file, 'w+') as f:
            while self.writing:
                value = await self.queue.get()
                influxdb_handler.write(value)


if __name__ == '__main__':
    app = DataService("data.csv")
    influxdb_handler = InfluxClient(
        INFLUXDB_IP,
        INFLUXDB_PORT,
        INFLUXDB_USER_NAME,
        INFLUXDB_PASSWORD,
        INFLUXDB_DB_NAME
    )
    app.start()
