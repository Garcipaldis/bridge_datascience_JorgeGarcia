import os, sys
import json

class Folders:

    @staticmethod
    def read_json(fullpath):
        """ Reads json file and returns it.
        """
        with open(fullpath, "r") as json_file_readed:
            json_readed = json.load(json_file_readed)
        return json_readed

    @staticmethod
    def add_path(num, jupyter=True):
        '''Adds a path to sys.
        Args:
            - num: number of times to get the dirname until reaching the rootpath.
        '''
        if jupyter:
            dirpath = os.getcwd()
        else:
            dirpath = __file__ # en caso de jupyter se usa os.getcwd()
        for i in range(num):
            dirpath = os.path.dirname(dirpath)
        sys.path.append(dirpath)

        return dirpath