# -*- coding: utf-8 -*-
import csv
from datetime import datetime


class CSV_writter:
    def __init__(self, file_path, field_names):
        '''
        :param file_path: type: str
        :param field_names: type: list
        '''
        self.file_path = file_path
        self.field_names = field_names

    def __write(self, data):
        with open(self.file_path, "a", newline='') as out_file:
            writer = csv.DictWriter(out_file, delimiter=';', fieldnames=self.field_names)
            writer.writerow(data)

    def __data_preparation(self, value):
        return dict(
            [x for x in zip(self.field_names, [
                datetime.strftime(datetime.now(), "%Y.%m.%d"),
                datetime.strftime(datetime.now(), "%H:%M:%S"),
                value
            ])]
        )

    def create_csv(self):
        with open(self.file_path, "w", newline='') as out_file:
            writer = csv.DictWriter(out_file, delimiter=';', fieldnames=self.field_names)
            writer.writeheader()

    def write_value(self, value):
        self.__write(self.__data_preparation(value))
