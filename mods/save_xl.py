from xlsxwriter import format, workbook, worksheet, chart_bar
from mods.err_report import *


class DataToXL:
    def __init__(self, file, exceptions, processed_boxes, with_plates, boxes_status, data_list):
        self.__file = file
        self.__exceptions = exceptions
        self.__processed_boxes = processed_boxes
        self.__with_plates = with_plates
        self.__boxes_status = boxes_status
        self.__data_list = data_list.copy()
        # self.__errors_list = errors_list
        # self.__remarks_list = remarks_list
        # Start from the first cell. Rows and columns are zero indexed.
        self.__row = 0
        self.__col = 0
        self.__length_columns = [[], []]  # replaces self.__length_1st_column and self.__length_1nd_column

        self.__workbook = workbook.Workbook  # <class 'xlsxwriter.workbook.Workbook'>
        self.__worksheet = worksheet.Worksheet  # < class 'xlsxwriter.worksheet.Worksheet'>
        self.__worksheet_error = worksheet.Worksheet
        self.__worksheet_remark = worksheet.Worksheet
        self.__chart_error = chart_bar.ChartBar
        self.__chart_remark = chart_bar.ChartBar
        self.__bold = format.Format

        self.__chart_type = {'type': 'bar'}  # , 'subtype': 'percent_stacked'}
        self.__chart_scale = {'x_scale': 2, 'y_scale': 2}

        self.__chart_style = 42
        self.__chart_legend = {'none': True}

    def __setup_workbook(self):
        # Workbook() takes one, non-optional, argument
        # which is the filename that we want to create.
        self.__workbook = workbook.Workbook(self.__file, {'strings_to_numbers': True})

        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        self.__worksheet = self.__workbook.add_worksheet(name="Summary")  # name=dt.today().strftime("%y%m%d"))
        self.__worksheet_error = self.__workbook.add_worksheet(name="Errors Chart")
        self.__worksheet_remark = self.__workbook.add_worksheet(name="Remarks Chart")
        self.__chart_error = self.__workbook.add_chart(self.__chart_type)
        self.__chart_remark = self.__workbook.add_chart(self.__chart_type)
        self.__bold = self.__workbook.add_format({'bold': True})

    def __write_headers(self, lst, text):
        try:
            for item, value in lst:
                if item == text:
                    self.__worksheet.write(self.__row, self.__col, item, self.__bold)
                else:
                    self.__worksheet.write(self.__row, self.__col, item)
                self.__worksheet.write(self.__row, self.__col + 1, value)
                self.__row += 1
        except Exception:
            report_feedback("Error Writing Headers", get_error_details(), 2)

    def __set_chart(self, chart, val, cat, title):
        try:
            chart.add_series({'values': val, 'categories': cat, 'data_labels': {'value': True}})
            chart.set_style(self.__chart_style)
            chart.set_legend(self.__chart_legend)
            chart.set_title({'name': title})
        except Exception:
            report_feedback("Error Setting Chart", get_error_details(), 2)

    def __write_data(self, lst):
        try:
            for item, value in lst:
                self.__worksheet.write(self.__row, self.__col, item)
                self.__worksheet.write(self.__row, self.__col + 1, value)
                self.__row += 1

        except Exception:
            report_feedback("Error Writing Data", get_error_details(), 2)

    def __unpack_list(self, lst):
        for j in range(2):
            self.__length_columns[j] += [len(str(i[j])) for i in lst]

    def __set_column_width(self, lst_headers):
        for i in range(2):
            self.__length_columns[i] = [len(str(item[i])) for item in lst_headers]

        for i in range(2):
            self.__unpack_list(self.__data_list[i].items())
        # self.__unpack_list(self.__errors_list.items())
        # self.__unpack_list(self.__remarks_list.items())

        for i in range(2):
            self.__worksheet.set_column(i, i, max(self.__length_columns[i]))

    def save_xl_file(self):
        """Save collected data to excel file"""
        try:
            self.__setup_workbook()
            # Use the worksheet object to write
            # data via the write() method.
            header_cells = (['Total Processed Boxes:', self.__processed_boxes],
                            ["Boxes with license plate:", self.__with_plates],
                            ['Transport order status', ", ".join([str(i) for i in self.__boxes_status])], ['', ''],
                            ["Results by error:", ""])

            error_cells = list(self.__data_list[0].items())
            separator_cells = (['', ''], ["Results by remark:", ""])
            remark_cells = list(self.__data_list[1].items())

            self.__set_column_width(header_cells)

            # Iterate over the data and write it out row by row.
            self.__write_headers(header_cells, "Results by error:")

            range_error = '!$B$' + str(self.__row + 1)
            self.__write_data(error_cells)
            range_error += ':$B$' + str(self.__row)

            self.__write_headers(separator_cells, "Results by remark:")

            range_remark = '!$B$' + str(self.__row + 1)
            self.__write_data(remark_cells)

            range_remark += ':$B$' + str(self.__row)

            self.__set_chart(self.__chart_error, '=' + self.__worksheet.get_name() + range_error,
                             '=' + self.__worksheet.get_name() + range_error.replace('B', 'A'),
                             'Processed boxes by ERROR (' + str(self.__exceptions) + ')')

            self.__set_chart(self.__chart_remark, '=' + self.__worksheet.get_name() + range_remark,
                             '=' + self.__worksheet.get_name() + range_remark.replace('B', 'A'),
                             'Processed boxes by REMARK (' + str(self.__exceptions) + ')')

            self.__worksheet_error.insert_chart('B2', self.__chart_error, self.__chart_scale)
            self.__worksheet_remark.insert_chart('B2', self.__chart_remark, self.__chart_scale)
        except Exception:
            report_feedback("Error Saving File", get_error_details(), 2)
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, f_name, exc_tb.tb_lineno)
            # Finally, close the Excel file
            # via the close() method.
        finally:
            self.__workbook.close()
