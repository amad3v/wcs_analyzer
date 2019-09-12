import csv
from mods.err_report import *

class WCS:
    def __init__(self, lst):
        self.__lst = lst
        self.__single_file = []
        self.__headers = []
        self.__boxes = 0
        self.__plates = 0
        self.__exceptions_list = []
        self.__all_exceptions = 0
        self.__get_csv_data()

    def __read_file(self, file):
        self.__single_file = []

        with open(file, 'r', newline='') as f:
            r = csv.reader(f, delimiter=',', quotechar='"')
            head = next(r, None)
            if not self.__headers:
                self.__headers = head.copy()

            for row in r:
                self.__single_file.append(row)

    def __get_csv_data(self):
        boxes = 0
        plates = 0
        exceptions = []

        for file in self.__lst:
            self.__read_file(file)
            boxes += len(self.__single_file)
            plates += len([i for i in self.__single_file if i[2] != ''])
            exceptions += [[i[19], i[23], i[3]] for i in self.__single_file if
                           i[7] == "EXCEPTION1" or i[7] == "EXCEPTION2"]

        self.__boxes = boxes
        self.__plates = plates
        self.__exceptions_list = exceptions
        self.__all_exceptions = len(exceptions)
        self.__replace_blanks()

    def __replace_blanks(self):
        for i in range(len(self.__exceptions_list)):
            # j += 1
            if not self.__exceptions_list[i][0]:# == '':
                self.__exceptions_list[i][0] = 'No Remark'
            if not self.__exceptions_list[i][1]:# == '':
                self.__exceptions_list[i][1] = 'No Error'

    def get_total_boxes(self):
        return self.__boxes

    def get_total_plates(self):
        return self.__plates

    def get_total_exceptions(self):
        return self.__all_exceptions

    def get_list_count(self, index):
        dic = {}

        for item in self.__exceptions_list:
            if item[index] in dic:
                dic[item[index]] += 1
            else:
                dic[item[index]] = 1
        return dic

    # return a list of a unique values in a specific column
    def get_unique_list(self):
        return list(set([i[2] for i in self.__exceptions_list]))

