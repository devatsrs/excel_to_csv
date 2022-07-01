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
        self.source_xls_path = (source_xls_path)
        self.dest_csv_path = (dest_csv_path)
        # self.source_xls_path = os.path.abspath(source_xls_path)
        # self.dest_csv_path = os.path.abspath(dest_csv_path)

    def convert(self):
        self.parsed_data = import_xls.parse_file(file_path=self.source_xls_path,orig_name=os.path.basename(self.source_xls_path))
        # print(self.parsed_data[1])
        # exit()

    def prepare(self):
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
        self.csv_rows = [] 
        # csv_rows = [[ ['#' for col in range(cols)] for col in range(rows)] for row in range(sheets)]


        # print(csv_rows[tables-1][rows-1][cols - 1])
        # pprint.pprint(csv_rows)
        # exit()
        # Prepare csv data 
        for sheet_index, x in enumerate(self.parsed_data[1]):
            sheet_name = x["table_name"]
            # sheets.append(sheet_name)

            # Filter extra sheets , setup header 
            if( sheet_name ==  "Terms and Conditions"):
                print(sheet_name + " Sheet Removed")
                continue

            if(not header):
                for y in x["column_metadata"]:
                    header.append(y["id"])

            # fix for header less sheets 
            _row = dict()
            for index,data in enumerate(x["column_metadata"]):
                if(len(header) > index and not data["id"] in header):
                    _row.update({header[index]: data["id"]})
            # insert                     
            if(_row):
                self.csv_rows.append(_row)
            
            # print(sheet_index)
            # print(header)
            # exit()

            # print(x["table_data"])
            # exit()
            """
            Convert list to rows
            [
                [
                    "Wired Microphones-Recording",
                    "USB",
                    "C44-USB",
                    "AKG-C22-USB"
                ],
                [
                    "",
                    "",
                    "Wired Mics",
                    "Wired Mics"
                ],
            ]
            to    
            {
                ('RRC-4SP', '19" RACK CASE, 4U SPACE', 761294218389.0, 249.99, 156.25), 
                ('PSB-7U', 'AC ADAPTOR (Order as Part #5100047496 this includes AC cord)', 5100047496.0, 40.11, 28.65),
                ...
            }  
            """
            # THIS HAS OPEN ISSUE:
            # WHEN THERE IS PARRALEL TABLE LIKE IN Philips I Dealer Q2 2022 Pricing_April 11 2022 (1).xlsx - SHEET - Extended Warranty IT WILL MERGE IT 
            rows = zip(*x["table_data"])
            # print(set(rows))
            # exit()
            # pprint.pprint(list(rows))
            # pprint.pprint((*x["table_data"]))

            """
                Loop through rows 
                prepare new row with required format 
                and append in new variable `csv_rows`
            
            """
            category = ""
            for row in rows:
                _row = dict() # {'name': 'Albania','area': 28748,   'country_code2': 'AL',  'country_code3': 'ALB'}

                # print(row)
                # print(x["row"][4][2])  # col , row
                # exit()
                # if not all(v for v in ('', '', '', '', '')):
                #     print("Yes FALSE")    
                # https://stackabuse.com/any-and-all-in-python-with-examples/
                """
                print(any([2 == 2, 3 == 2]))    => True
                print(any([True, False, False]))    => True
                print(any([False, False])) => False
                """
                
                if any(row):

                    """
                    Skip column name
                    """
                    if (row[0] == header[0]): # header row detected  ('Item Name', 'Item Code', 'List', 'Dealer', 'Weight', 'Length', 'Width', 'Height')
                        print("header row detected ", row)     
                        continue
                    
                    """
                    Check to identify category : if any column has empty values + check 2nd and 3rd col also blank
                    Record category : 
                    """
                    if (not all(row) and not row[1] and not row[2]): # and row[0] and  row[1]:
                        print("category = ", row[0] , len(row[1]) , len(row[2]) , row)     
                        category = row[0]
                        continue

                    for i, row_item in enumerate(row):
                        # print(row_item)
                        # print(i)
                        # print (f'header[{col_index}]: {row_item}')
                        if(len(header) > i):
                            _row.update({header[i]: row_item})

                    # add sheet name as extra field
                    # and uppend row to csv  row
                    if category :
                        _row.update({"ext_category": category})        

                    _row.update({"sheet_name": sheet_name})


                    self.csv_rows.append(_row)
                else:
                    print(row , "All empty")
       

        # print(sheets)
        # print(header)
        # print(list(csv_rows))

        # header.pop()
        #csv header 
        header.append("sheet_name") # ['name', 'area', 'country_code2', 'country_code3']
        header.append("ext_category") 
        self.header = header
        # self.csv_rows = csv_rows
        # pprint.pprint(header)
        # pprint.pprint(csv_rows)
        # exit()

         

    def write(self):
 
        # print(csvfilepath)
        with open(self.dest_csv_path, 'w', encoding='UTF8', newline='') as f:
            # writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer = csv.DictWriter(f, fieldnames=self.header)
            writer.writeheader()
            # print(self.csv_rows)
            # exit()
            writer.writerows(self.csv_rows)

# argument for souce filename 
# argument for destination filename
source_xls_path = sys.argv[1]
dest_csv_path = sys.argv[2]
# print(source_xls_path)
# print(dest_csv_path)

# xlsObj = XlsToCsv('test_excel.xlsx')
xlsObj = XlsToCsv(source_xls_path , dest_csv_path)

print(xlsObj.source_xls_path)
print(xlsObj.dest_csv_path)

# $ py ./xls_to_csv.py ./excel/AVR\ Pricelist\ -\ Roland\ Pro\ AV\ Jan\ 24th\ 2022.xlsm ./csv/AVR\ Pricelist\ -\ Roland\ Pro\ AV\ Jan\ 24th\ 2022.csv
# $ py ./xls_to_csv.py ./excel/AVR\ Pricelist\ -\ Roland\ Pro\ AV\ Jan\ 24th\ 2022.xlsm ./csv/AVR\ Pricelist\ -\ Roland\ Pro\ AV\ Jan\ 24th\ 2022.csv
# exit()

# xlsObj = XlsToCsv('Harman Pro Pricing 010522.xlsx')
# xlsObj = XlsToCsv("EAW Dealer Price List April 2022.xlsx")
# xlsObj = XlsToCsv("DMR Price List 1-1-2022.xlsx")
# xlsObj = XlsToCsv("AVR Pricelist - Roland Pro AV Jan 24th 2022.xlsm")
# xlsObj = XlsToCsv("Visionary Solutions - Dealer Price List - Effective Feb 15 2022.xlsx")
xlsObj.convert()
xlsObj.prepare()
xlsObj.write()
# print (xlsObj.csvfilepath[0])




# db = DB()
# print(xlsObj.csvfilepath[0])
# db.insert(title="test_excel",columns=xlsObj.header,csvpath=os.path.normpath(xlsObj.csvfilepath[0]))
