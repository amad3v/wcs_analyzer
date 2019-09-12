import json
from pathlib import Path


class Settings:
    __fail_safe_path: Path

    def __init__(self):
        self.__settings_path = Path.home()  # os.path.expanduser('~') # = os.path.dirname(os.path.realpath(__file__))
        # os.path.join(self.__settings_path, 'settings.json')
        self.__settings_file = self.__settings_path.joinpath('settings.json')
        self.__exist = False
        self.file_exit()
        # default path, in case settings.json doesn't exist
        self.__fail_safe_path = str(self.__settings_path.joinpath('Desktop'))
        # if os.name=='posix':
        #     self.__fail_safe_path = os.path.expanduser("~/Desktop")
        # if os.name=='nt':
        #     self.__fail_safe_path = os.path.expanduser("~\\Desktop")
        self.__paths = {}  # {'open':'','save':''}
        self.load_settings()

    def file_exit(self):
        # check if the file exists
        # self.__exist = os.path.isfile(self.__settings_file)
        self.__exist = self.__settings_file.is_file()

    def load_settings(self):
        if self.__exist:
            with open(str(str(self.__settings_file)), 'r') as file:
                self.__paths = json.load(file)
        else:
            self.__paths = {'open': self.__fail_safe_path, 'save': self.__fail_safe_path}

    def save_settings(self):
        with open(str(self.__settings_file), 'w') as file:
            json.dump(self.__paths, file)

    def set_path(self, typ, path):
        self.__paths[typ] = str(Path(path).parent)

    def get_path(self, typ):
        return self.__paths[typ]
