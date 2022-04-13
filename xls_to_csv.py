import os
from lib import import_xls


def _get_excce(filename):
    return [os.path.dirname(__file__) + "/excel/" + filename, filename]


class XlsToCsv():

    def __init__(self, filename):
        self.filename = filename

    def convert(self):
        # # print(self.filename)
        # filepath = os.path.dirname(__file__) + "/excel/" + self.filename
        # print(self.filename)
        filepath_n_name = _get_excce(self.filename)
        # print(filepath)
        # exit()
        # parsed_file = import_xls.parse_file(*_get_excce(self.filename))
        parsed_file = import_xls.parse_file(*filepath_n_name)
        print(parsed_file)


xlsObj = XlsToCsv('test_excel.xlsx')
xlsObj.convert()
