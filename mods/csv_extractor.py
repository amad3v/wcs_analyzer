import csv
# from itertools import chain
from mods.err_report import *


class WCS1:
    def __init__(self, files_list):
        """Initialize WCS instance

        Keyword arguments:
        files_list -- list of csv files to process
        """
        self.__files_list = files_list
        self.__unified_data = []  # iter([])  # set to empty iterator of lists
        self.__headers = []
        self.__boxes = 0
        self.__plates = 0
        self.__exceptions_list = []
        self.__all_exceptions = 0
        self.__get_csv_data()

    def __read_file(self, file):
        # clear list from previous data
        self.__unified_data = []
        # the file starts with \ufeff
        # to remove it, the encoding must be set to utf-8-sig
        with open(file, 'r', newline='', encoding='utf-8-sig') as f:
            # creates a generator of lists
            lines = (line for line in csv.reader(f, delimiter=',', quotechar='"'))

            # select 1st row: columns titles (headers)
            head = next(lines, None)

            # creates a generator of dictionary by zipping head to every entry
            data_dicts = (dict(zip(head, data)) for data in lines)

            # creates a list of target data
            # consider a generator // issue: getting the total number of rows
            target_data = [
                [data_dict['Licenceplate'], data_dict['Transport order status'], data_dict['Last station'],
                 data_dict['Remark'], data_dict['Error ID']]
                for data_dict in data_dicts
            ]

            # chaining generators
            # chain(self.__unified_data, target_data)
            self.__unified_data = target_data.copy()

    def __get_csv_data(self):
        """Extract necessary data from CSV files"""
        boxes = 0
        plates = 0
        # exceptions = []

        files = (file for file in self.__files_list)

        for file in files:
            self.__read_file(file)
            boxes += len(self.__unified_data)
            plates += len([i for i in self.__unified_data if i[0] != ''])
            self.__exceptions_list += [i for i in self.__unified_data if i[2] == 'EXCEPTION1' or i[2]=='EXCEPTION2']

        self.__boxes = boxes  # managed by get_total_boxes
        self.__plates = plates  # managed by get_total_plates
        # self.__exceptions_list = exceptions # used by get_list_count/get_unique_list/replace_blanks
        self.__all_exceptions = len(self.__exceptions_list)  # managed by get_total_exceptions
        self.__replace_blanks()

    def __replace_blanks(self):
        """Replace empty fields with meaningful data"""
        for i in self.__exceptions_list:  # range(len(self.__exceptions_list)):
            # j += 1
            if not i[3]: i[3] = 'No Remark'  # == ''
            if not i[4]: i[4] = 'No Error'  # == ''

    def get_total_boxes(self):
        """Return the total number of processed boxes/cartons"""
        return self.__boxes

    def get_total_plates(self):
        """Return the number of orders with license plate"""
        return self.__plates

    def get_total_exceptions(self):
        """Return the total number of exceptions"""
        return self.__all_exceptions

    def get_list_count(self, key):
        """Return a dict of the numbers of entries under <key>

        Keyword arguments:
        key -- key of items to count
        """
        dic = {}

        for item in self.__exceptions_list:
            dic[item[key]] = dic.setdefault(item[key], 0) + 1

        return dic

    def get_unique_list(self):
        """Return a list of a unique values in a specific column"""
        return list(set([i[1] for i in self.__exceptions_list]))
