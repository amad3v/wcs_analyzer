import ctypes
# import os (pathlib is used instead)
import linecache
import sys
# from typing import Union, Any, List
from pathlib import Path
import time

from mods import fixqt

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from mods.csv_extractor import WCS1
from mods.csvextractor import WCS
from mods.save_xl import DataToXL
from mods.params import Settings
from mods.err_report import *
from ui.mainwindow import Ui_mwWCS

# pathlib.WindowsPath, for posix OSs (linux, macOS) use PosixPath
# os.path.join(os.environ["HOMEPATH"], "Desktop")
# home = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# if os.name == 'posix':
#     home = os.path.expanduser("~/Desktop")
# if os.name == 'nt':
#     home = os.path.expanduser("~\\Desktop")
home = str(Path.home().joinpath('Desktop'))

# icon_path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ui"), "Icon.ico")
open_filter = "CSV files (*.csv)"
save_filter = "Excel Workbook (*.xlsx)"


def create_icon():
    try:
        app_icon = QIcon()

        full_path = Path('.').absolute().joinpath('ui')
        # os.path.join(os.path.dirname(os.path.realpath(__file__)), "ui")
        app_icon.addFile(str(full_path.joinpath('i16.png')), QtCore.QSize(16, 16))
        app_icon.addFile(str(full_path.joinpath('i24.png')), QtCore.QSize(24, 24))
        app_icon.addFile(str(full_path.joinpath('i32.png')), QtCore.QSize(32, 32))
        app_icon.addFile(str(full_path.joinpath('i48.png')), QtCore.QSize(48, 48))
        app_icon.addFile(str(full_path.joinpath('i128.png')), QtCore.QSize(12, 128))
        app_icon.addFile(str(full_path.joinpath('i256.png')), QtCore.QSize(256, 256))

        return app_icon
    except Exception:
        report_error("Error occurred (Icon)", get_error_details())


class MainWindow(QtWidgets.QMainWindow):  # window = qtw.QMainWindow()
    def __init__(self, window_title="", open_filter="All files (*.*)", save_filter="All files (*.*)", parent=None):
        super().__init__(parent)
        self.__window_title = window_title  # window.setWindowTitle("Student Manager")
        self.ui = Ui_mwWCS()  # ui_window = Ui_mwWCS()
        self.ui.setupUi(self)  # ui_window.setupUi(window)
        self.__app_settings = Settings()  # mw_home
        self.__open_files = open_filter
        self.__save_files = save_filter
        self.__excel_file = ""
        self.setWindowIcon(create_icon())  # QIcon(icon_path))
        self.__csv_files_list = []

    def __show_open_dialog(self):
        """Called from on_add_clicked to open file dialog to select CSV files"""
        self.__csv_files_list, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open files',
                                                                          self.__app_settings.get_path('open'),
                                                                          self.__open_files)

        self.__csv_files_list = [str(Path(item)) for item in self.__csv_files_list]

    def __show_save_dialog(self):
        """Called from on_save_clicked to save excel file"""
        xlfile, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as', self.__app_settings.get_path('save'),
                                                          self.__save_files)

        return xlfile

    def on_add_clicked(self):
        # list_names = QtWidgets.QFileDialog(window, "Open files", home, "CSV files (*.csv)")
        # return (type List) contains:
        # 1. list of selected files, type: List
        # 2. filter (type str)
        # list_names, _ = self.__show_open_dialog()
        self.__show_open_dialog()
        self.ui.lstInput.addItems(self.__csv_files_list)
        if self.__csv_files_list:
            self.__app_settings.set_path('open', self.__csv_files_list[-1])
        elif self.ui.lstInput.count():
            self.__csv_files_list = [self.ui.lstInput.item(i) for i in range(self.ui.lstInput.count())]

    def on_save_clicked(self):
        try:
            if len(self.__csv_files_list) == 0:
                raise EmptyList

            xl_file = self.__show_save_dialog()

            # raise error if no file selected/created
            if xl_file == '':
                raise NoTargetFile

            # update settings file
            self.__app_settings.set_path('save', xl_file)
            self.__excel_file = xl_file

            # create WCS object
            #csv_wcs = WCS(self.__csv_files_list)
            csv_wcs = WCS1(self.__csv_files_list)

            boxes = csv_wcs.get_total_boxes()
            plates = csv_wcs.get_total_plates()
            total_exceptions = csv_wcs.get_total_exceptions()
            err_list = csv_wcs.get_list_count(4)#1
            # err_list = csv_wcs.get_list_count(1)#1
            rem_list = csv_wcs.get_list_count(3)#0
            # rem_list = csv_wcs.get_list_count(0)#0
            status = csv_wcs.get_unique_list()


            results = DataToXL(xl_file, total_exceptions, boxes, plates, status, err_list, rem_list)
            results.save_xl_file()

            report_task("File operation", "Excel file generated and saved\n" + str(Path(self.__excel_file)))
            # report_task("Execution time", str(
            # round(duration, 7)) + " seconds to:\nProcess 283 808 rows x 36 columns\nand 22 286 iterations in 47 files")
            # report_task("Execution time",
            #             str(round(duration, 7)) + " seconds to:\nProcess " + "{:,d}".format(boxes).replace(",", ' ') +
            #             " rows x 36 columns\nand " + "{:,d}".format(csv_wcs.loops).replace(",", ' ') + ' iteration')

        except NoTargetFile:
            report_error("Error occurred", "No target file!\nPlease enter file name")
        except EmptyList:
            report_error("Error occurred", "Empty list not allowed!\nPlease add CSV files")
        except Exception:
            report_error("Error occurred (SAVE)", get_error_details())

    def set_excel_file(self, file):
        self.__excel_file = file


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow("WCS Analyzer", open_filter, save_filter)
    window.ui.pbAdd.clicked.connect(window.on_add_clicked)
    window.ui.pbSave.clicked.connect(window.on_save_clicked)

    window.show()

    sys.exit(app.exec_())
