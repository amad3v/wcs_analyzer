"""Manage application settings"""
import shelve
from pathlib import Path


class Settings:
    __fail_safe_path: Path

    def __init__(self):
        # os.path.expanduser('~') # = os.path.dirname(os.path.realpath(__file__))
        # initial path set to HOME (for saving settings)
        self.__settings_path = Path.home()
        # os.path.join(self.__settings_path, 'settings.json')
        # settings file (full path) .../settings.db
        self.__settings_file = self.__settings_path.joinpath('settings')
        self.__exist = False
        self.__file_exit()
        # default path, in case settings.dat doesn't exist (e.g. 1st launch)
        # joins the path in __settings_path to Desktop folder
        self.__fail_safe_path = str(self.__settings_path.joinpath('Desktop'))
        # open: last opened directory (input files / open)
        # save: last opened directory (output file / save)
        self.__paths = {}  # {'open':'','save':''}
        self.__load_settings()

    def __file_exit(self):
        # check if the file exists
        # self.__exist = os.path.isfile(self.__settings_file)
        self.__exist = self.__settings_path.joinpath('settings.dat').is_file()

    def __load_settings(self):
        if self.__exist:
            with shelve.open(str(self.__settings_file)) as db:
                self.__paths = {'open': db['open'], 'save': db['save']}
        else:
            self.__paths = {'open': self.__fail_safe_path, 'save': self.__fail_safe_path}

    def __save_settings(self):
        with shelve.open(str(self.__settings_file)) as db:
            db['open'] = self.__paths['open']
            db['save'] = self.__paths['save']

    def set_path(self, dialog_type, path):
        """Save a directory path.

        Keyword arguments:
        dialog_type -- 'open' or 'save' (string)
        path -- path to save (string)
        """
        self.__paths[dialog_type] = str(Path(path).parent)
        self.__save_settings()

    def get_path(self, dialog_type):
        """Return a directory path.

        Keyword arguments:
        dialog_type -- 'open' or 'save' (string)
        """
        return self.__paths[dialog_type]
    
