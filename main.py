# import linecache
# import sys
# from typing import Union, Any, List
from pathlib import Path, WindowsPath
# import time
from mods import fixqt

import ctypes

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from mods.csv_extractor import WCS
from mods.err_report import *
from mods.params import Settings
from mods.save_xl import DataToXL
from ui.mainwindow import Ui_mwWCS

# =======================================#
# the following is to make the app icon  #
# visible in the task bar                #
# =======================================#
if type(Path.home()) == WindowsPath:
    # if os.name == 'nt':
    app_id = 'mj.wcs_analyzer_xx.gui.1.0'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
# =======================================#

# pathlib.WindowsPath, for posix OSs (linux, macOS) use PosixPath
# os.path.join(os.environ["HOMEPATH"], "Desktop")
# home = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# if os.name == 'posix':
#     home = os.path.expanduser("~/Desktop")
# if os.name == 'nt':
#     home = os.path.expanduser("~\\Desktop")
home = str(Path.home().joinpath('Desktop'))

icon_path = str(Path(Path(Path(__file__).parent).joinpath('ui')).joinpath('Icon.ico'))
open_filter = "CSV files (*.csv)"
save_filter = "Excel Workbook (*.xlsx)"


class MainWindow(QtWidgets.QMainWindow):  # window = qtw.QMainWindow()
    def __init__(self, window_title="", op_filter="All files (*.*)", sv_filter="All files (*.*)", parent=None):
        super().__init__(parent)
        self.__window_title = window_title  # window.setWindowTitle("Student Manager")
        self.ui = Ui_mwWCS()  # ui_window = Ui_mwWCS()
        self.ui.setupUi(self)  # ui_window.setupUi(window)
        self.__app_settings = Settings()  # mw_home
        self.__open_files = op_filter
        self.__save_files = sv_filter
        self.__excel_file = ""
        self.setWindowIcon(QIcon(icon_path))
        self.__csv_files_list = []

    def __show_open_dialog(self):
        """Called from on_add_clicked to open file dialog to select CSV files"""
        files_list, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open files',
                                                               self.__app_settings.get_path('open'),
                                                               self.__open_files)

        self.__csv_files_list = [str(Path(item)) for item in files_list]

    def __show_save_dialog(self):
        """Called from on_save_clicked to save excel file"""
        xlfile, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as',
                                                          self.__app_settings.get_path('save'),
                                                          self.__save_files)

        return xlfile

    def on_clear_clicked(self):
        self.__csv_files_list.clear()

    def on_add_clicked(self):
        # list_names = QtWidgets.QFileDialog(window, "Open files", home, "CSV files (*.csv)")
        # return (type List) contains:
        # 1. list of selected files, type: List
        # 2. op_filter (type str)
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

            # create WCS object
            csv_wcs = WCS(self.__csv_files_list)

            if not csv_wcs.get_total_exceptions:
                report_feedback("Data processing", 'No data available\nProducts at exception lanes = 0')
                return

            self.__excel_file = self.__show_save_dialog()
            # raise error if no file selected/created
            if self.__excel_file == '':
                raise NoTargetFile

            if Path(self.__excel_file).suffix != '.xlsx':
                self.__excel_file += '.xlsx'

            # update settings file
            self.__app_settings.set_path('save', self.__excel_file)

            # results = DataToXL(xl_file, total_exceptions, boxes, plates, status, [err_list, rem_list])
            results = DataToXL(self.__excel_file, csv_wcs.get_total_exceptions,
                               csv_wcs.get_total_boxes,
                               csv_wcs.get_total_plates,
                               csv_wcs.get_unique_list,
                               [csv_wcs.get_list_count(4), csv_wcs.get_list_count(3)])

            results.save_xl_file()

            report_feedback("File operation", "Excel file generated and saved\n" + str(Path(self.__excel_file)))

        except NoTargetFile:
            report_feedback("Error occurred", "No target file!\nPlease enter file name", 2)
        except EmptyList:
            report_feedback("Error occurred", "Empty list not allowed!\nPlease add CSV files", 2)
        except Exception:
            report_feedback("Error occurred (SAVE)", get_error_details(), 2)

    def __xl_file(self):
        file = self.__show_save_dialog()
        try:
            # raise error if no file selected/created
            if file == '':
                raise NoTargetFile

            if Path(file).suffix != '.xlsx':
                file += '.xlsx'

            # update settings file
            self.__app_settings.set_path('save', file)

            self.__excel_file = file
        except NoTargetFile:
            report_feedback("Error occurred", "No target file!\nPlease enter file name", 2)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow("WCS Analyzer", open_filter, save_filter)
    window.ui.pbAdd.clicked.connect(window.on_add_clicked)
    window.ui.pbSave.clicked.connect(window.on_save_clicked)
    window.ui.pbClearList.clicked.connect(window.on_clear_clicked)

    window.show()

    sys.exit(app.exec_())
