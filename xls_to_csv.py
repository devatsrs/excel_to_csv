import json
import os
import sys
from lib import import_xls
import csv
import pprint

# from lib.db import DB


# def _get_excce(filename, folder):
#     return [os.path.dirname(__file__) + "/"+folder + "/" + filename, filename]


class XlsToCsv():

    def __init__(self, source_xls_path, dest_csv_path):
        self.source_xls_path = os.path.abspath(source_xls_path)
        self.dest_csv_path = os.path.abspath(dest_csv_path)

    def convert(self):
        # # print(self.source_xls_path)
        # filepath = os.path.dirname(__file__) + "/excel/" + self.source_xls_path
        # print(self.source_xls_path)
        # filepath_n_name = _get_excce(self.source_xls_path, "excel")
        # print(filepath_n_name)
        filepath_n_name = [self.source_xls_path,os.path.basename(self.source_xls_path)]
        # print(filepath_n_name)
        # exit()
        # parsed_file = import_xls.parse_file(*_get_excce(self.source_xls_path))
        # self.parsed_data = import_xls.parse_file(*filepath_n_name)
        self.parsed_data = import_xls.parse_file(file_path=self.source_xls_path,orig_name=os.path.basename(self.source_xls_path))
        # print(self.parsed_data[1])
        # exit()

    def write(self):

        # print(self.parsed_data[1])
        # json_data = json.loads(self.parsed_data[1])
        # print(json_data)
        # exit()
        header = []
        sheets = []
        # +1 for sheet name
        # cols = (len(self.parsed_data[1][0]["column_metadata"])) + 1
        # rows = (len(self.parsed_data[1][0]["table_data"][0]))
        # tables = (len(self.parsed_data[1]))  # sheets
        # print(cols)
        # print(rows)
        # print(tables)
        # exit()
        # csv_rows = list()
        # csv_rows = [[[""]*cols]*rows]*tables
        csv_rows = [] 
        # csv_rows = [[ ['#' for col in range(cols)] for col in range(rows)] for row in range(sheets)]

        # print(csv_rows[tables-1][rows-1][cols - 1])
        # pprint.pprint(csv_rows)
        # exit()
        for sheet_index, x in enumerate(self.parsed_data[1]):
            sheet_name = x["table_name"]
            sheets.append(sheet_name)
            # print(sheet_index)
            # print(sheet_name)
            
            for y in x["column_metadata"]:
                if(sheet_index == 0):
                    header.append(y["id"])

            # print(x["table_data"])
            # exit()
            table_data1 = zip(*x["table_data"])

            # pprint.pprint(list(table_data1))
            # pprint.pprint((*x["table_data"]))
            for table_data in table_data1:
                _row = dict() # {'name': 'Albania','area': 28748,   'country_code2': 'AL',  'country_code3': 'ALB'}

                # print(table_data)
                # print(x["table_data"][4][2])  # col , row
                # exit()
                for row_index, table_row_item in enumerate(table_data):
                    # print(table_row_item)
                    # print(x["table_data"][col_index][row_index])  # col , row
                    # print(row_index)
                    # csv_rows[sheet_index][row_index][col_index] = table_row_item
                    # print (f'csv_rows[{sheet_index}][{row_index}][{col_index}] = {table_row_item}')
                    # print (f'header[{col_index}]: {table_row_item}')
                    if(len(header) > row_index):
                        _row.update({header[row_index]: table_row_item})

                # add sheet name as extra field
                # and uppend row to csv  row
                _row.update({"sheet_name": sheet_name})
                csv_rows.append(_row)

        # print(sheets)
        # print(header)
        # csv_rows[1][1][1] = "sheet 1 row 0 col 0"
        # csv_rows[1][0][0] = "sheet 2 row 0 col 0"
        # print(list(csv_rows))

        # header.pop()
        #csv header 
        header.append("sheet_name") # ['name', 'area', 'country_code2', 'country_code3']
        self.header = header
        # self.csv_rows = csv_rows
        # pprint.pprint(header)
        # pprint.pprint(csv_rows)
        # exit()

        # csv data example 
        #   [
        #     {'name': 'Albania',
        #      'area': 28748,
        #      'country_code2': 'AL',
        #      'country_code3': 'ALB'},
        #     {'name': 'Algeria',
        #      'area': 2381741,
        #      'country_code2': 'DZ',
        #      'country_code3': 'DZA'},
        #     {'name': 'American Samoa',
        #      'area': 199,
        #      'country_code2': 'AS',
        #      'country_code3': 'ASM'}
        # ]
        # filename = (os.path.splitext(
        #     os.path.basename(self.source_xls_path))[0]) + ".csv"
        # # print("filename " + filename)
        # csvfilepath = _get_excce(filename, "csv")
        # self.csvfilepath = csvfilepath
        
        # print(csvfilepath)
        with open(self.dest_csv_path, 'w', encoding='UTF8', newline='') as f:
            # writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(csv_rows)

# argument for souce filename 
# argument for destination filename
source_xls_path = sys.argv[1]
dest_csv_path = sys.argv[2]
print(source_xls_path)
print(dest_csv_path)

# xlsObj = XlsToCsv('test_excel.xlsx')
xlsObj = XlsToCsv(source_xls_path , dest_csv_path)
# xlsObj = XlsToCsv('Harman Pro Pricing 010522.xlsx')
# xlsObj = XlsToCsv("EAW Dealer Price List April 2022.xlsx")
# xlsObj = XlsToCsv("DMR Price List 1-1-2022.xlsx")
# xlsObj = XlsToCsv("AVR Pricelist - Roland Pro AV Jan 24th 2022.xlsm")
# xlsObj = XlsToCsv("Visionary Solutions - Dealer Price List - Effective Feb 15 2022.xlsx")
xlsObj.convert()
xlsObj.write()
# print (xlsObj.csvfilepath[0])




# db = DB()
# print(xlsObj.csvfilepath[0])
# db.insert(title="test_excel",columns=xlsObj.header,csvpath=os.path.normpath(xlsObj.csvfilepath[0]))
