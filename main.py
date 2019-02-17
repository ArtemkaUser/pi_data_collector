import threading
from csv_writter import CSV_writter as csv
from const import *
# from easysnmp import snmp_get
import os


class App:
    def __init__(self, file_path, field_names):
        self.csv_handler = csv(file_path, field_names)
        if not os.path.isfile(file_path):
            self.csv_handler.create_csv()
        self.__write_value()

    def __write_value(self):
        threading.Timer(1, self.__write_value).start()
        self.csv_handler.write_value(self.__get_data())

    def __get_data(self):
        # data = snmp_get('1.3.6.1.4.1.40418.2.2.4.2', hostname='192.168.15.20', community='public', version=1)
        # return str(data).split("'")[1]
        return 91.02

    def post_data(self, get):
        pass


if __name__ == '__main__':
    app = App(FILE_PATH, FIELD_NAMES)
