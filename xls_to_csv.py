import json
import os
from lib import import_xls
import csv


def _get_excce(filename, folder):
    return [os.path.dirname(__file__) + "/"+folder + "/" + filename, filename]


class XlsToCsv():

    def __init__(self, filename):
        self.filename = filename

    def convert(self):
        # # print(self.filename)
        # filepath = os.path.dirname(__file__) + "/excel/" + self.filename
        # print(self.filename)
        filepath_n_name = _get_excce(self.filename, "excel")
        # print(filepath)
        # exit()
        # parsed_file = import_xls.parse_file(*_get_excce(self.filename))
        self.parsed_data = import_xls.parse_file(*filepath_n_name)
        # print(parsed_file)

    def write(self):

        # print(self.parsed_data[1])
        # json_data = json.loads(self.parsed_data[1])
        # print(json_data)
        # exit()
        for x in self.parsed_data[1]:
            print(x["table_name"])

        # csv header
        fieldnames = ['name', 'area', 'country_code2', 'country_code3']

        # csv data
        rows = [
            {'name': 'Albania',
             'area': 28748,
             'country_code2': 'AL',
             'country_code3': 'ALB'},
            {'name': 'Algeria',
             'area': 2381741,
             'country_code2': 'DZ',
             'country_code3': 'DZA'},
            {'name': 'American Samoa',
             'area': 199,
             'country_code2': 'AS',
             'country_code3': 'ASM'}
        ]
        filename = (os.path.splitext(
            os.path.basename(self.filename))[0]) + ".csv"
        print("filename " + filename)
        csvfilepath = _get_excce(filename, "csv")
        print(csvfilepath)
        with open(csvfilepath[0], 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


xlsObj = XlsToCsv('test_excel.xlsx')
xlsObj.convert()
xlsObj.write()
