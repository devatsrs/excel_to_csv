from cmath import log
import json
import os
import sys
from wsgiref import headers
from lib import import_xls
from lib.log  import Log
import csv
import pprint
from re import match


class XlsToCsv():

    def __init__(self, source_xls_path, dest_csv_path):
        self.source_xls_path = (source_xls_path)
        self.dest_csv_path = (dest_csv_path)
        self.header = dict([])
        self.csv_rows = []
        self.response = {}
        self.ALLOWED_BLANK_COL_NAMES = 50 # percentage 
        self.skip_sheets_list = [
            "Legal",  # Shure
            "Terms and Conditions",
            "Overview",
            "Navigation", # Leon-PriceGuide-COMM-2021-DLR
            "Cover", # B-Tech AV Mounts LLC Price List 2021 (Release 1.0) - Sapphire Partner
            "T of C", "How to","P.O.'s", "Demo", "Freight", "Service", "Warranty", "Contacts",  #
            "Traveler", # 2021 Price Sheet_Silver-Gold_210901-edit.xlsx ->  # Traveler Part Number Generator , Traveler Key
            "Lookups", # 2021 Price Sheet_Silver-Gold_210901-edit.xlsx ->  # Traveler Part Number Generator , Traveler Key, Pricing Lookups1
            "Specs", # All Terrain Stage System Price August 2021.xlsx
        ]
        self.log = Log()

    # Read exce file and load parsed data
    def parsed_excel(self):

        self.log.info("---")
        self.log.info("Parsing"+ self.source_xls_path)

        self.parsed_data = import_xls.parse_file(
            file_path=self.source_xls_path, orig_name=os.path.basename(self.source_xls_path))
        
        self.log.debug("parsed_excel done")
        

    def skip_sheets(self):
        return self.skip_sheets_list

    def should_skip_sheet(self, sheet_name):
        for word in self.skip_sheets():
            if word.lower().strip() in sheet_name.lower():
                return True

        return False

    def prepare_header_by_sheet(self):

        # in case blank title / header is found we will add __1__ as header
        _blank_col_index = 0
        for sheet_index, data in enumerate(self.parsed_data[1]):
            _header = []
            _dup_cols = []

            sheet_name = data["table_name"]
            if(self.should_skip_sheet(sheet_name)):
                self.log.debug(sheet_name + " Sheet Skipped")
                self.header[sheet_index] = _header
                continue

            for col in data["column_metadata"]:
                col_name = self.prepar_header_col(col["id"])

                if(col_name in _header):
                    _dup_cols.append(col_name)
                    # found count occurence of same col name
                    _dup_col_index = _dup_cols.count(col_name)
                    col_name = f"{col_name}_{_dup_col_index}"

                if(col_name):
                    _header.append(col_name)
                else:
                    _blank_col_index += 1
                    col_name = "__" + str(_blank_col_index) + "__"
                    _header.append(col_name)

            _header.append("sheet_name")
            _header.append("ext_category")
            self.header[sheet_index] = _header

    def prepare_header(self):

        # if (self.is_cav_dealer_file()):
        #     self.cav_dealer_prepare_header_by_sheet()
        # else:
        #     self.prepare_header_by_sheet()

        self.prepare_header_by_sheet()
 

        # look through dict and merge array
        self.all_sheet_headers = []
        for sheet_index in self.header:
            for h_index, h_text in enumerate(self.header[sheet_index]):
                if(h_text not in ["ext_category", "sheet_name"]):
                    if(h_text not in self.all_sheet_headers):
                        self.all_sheet_headers.append(h_text)

        self.header_vs_all_mapping = dict([])

        for ah_index, ah_text in enumerate(self.all_sheet_headers):
            f_header_index = []
            for sheet_index in self.header:
                if(ah_text in self.header[sheet_index]):
                    f_h_index = self.header[sheet_index].index(ah_text)
                    f_header_index.append(f_h_index)
                else:
                    f_header_index.append(-1)

            self.header_vs_all_mapping[ah_index] = f_header_index

        # Add extra cols
        self.all_sheet_headers.append("sheet_name")
        self.all_sheet_headers.append("ext_category")

        for h_index in self.header:
            # Detect how many empty cols detected __1__
            empty_cols_found = list(filter(lambda col: match('^__\d+__$', col) , self.header[h_index]))
            total_col = len(self.header[h_index]) 
            if total_col > 0 :
                percentage  = ( len(empty_cols_found) / total_col) * 100
                self.log.debug(f"empty_cols_found = {len(empty_cols_found)} total_col = {total_col} Percentage = {percentage} ")
                if( percentage >= self.ALLOWED_BLANK_COL_NAMES):
                    self.log.debug("self.header")
                    self.log.debug(self.header)
                    self.log.debug("self.all_sheet_headers")
                    self.log.debug(self.all_sheet_headers)
                    self.log.debug(len(self.all_sheet_headers))
                    self.log.debug("self.header_vs_all_mapping")
                    self.log.debug(self.header_vs_all_mapping)
                    self.log.debug(len(self.header_vs_all_mapping))

                    self.log.debug("Complex excel detected")
                    self.log.debug(len(empty_cols_found))
                    self.log.debug(empty_cols_found)

                    self.response["status"] = "failed"
                    self.response["message"] = "Complex excel detected"
                    self.response["file"] = self.source_xls_path
                    

        # exit()

    def header_less_row(self, data, header):

        # {'name': 'Albania','area': 28748,   'country_code2': 'AL',  'country_code3': 'ALB'}
        _row = dict()

        if(data["column_metadata"][0]["id"] not in header):
            for index, col in enumerate(data["column_metadata"]):
                row_text = self.prepar_header_col(col["id"])
                if(len(header) > index and row_text not in header):
                    _row.update({header[index]: col["id"]})

            # insert
            all_row_empty = all(
                element == "" for element in list(_row.values()))
            if(not all_row_empty):
                self.csv_rows.append(_row)

    def indexExists(self, list, index):
        if 0 <= index < len(list):
            return True
        else:
            return False

    def prepar_header_col(self, col_name):
        col_name = str(col_name).lower().strip()
        return col_name.replace('\n', " ")

    def is_header_col(self, row):

        for row_text in row:
            row_text = self.prepar_header_col(row_text)
            if (row_text in self.all_sheet_headers):
                return True

        return False

    def prepare_csv_rows(self):

        # prepare header first to load data in dict with key value pair
        self.prepare_header()

        # Loop through sheets and Prepare csv data
        for sheet_index, data in enumerate(self.parsed_data[1]):
            sheet_name = data["table_name"]

            # if(self.is_cav_dealer_file() and self.cav_ignore_sheets(sheet_name)):
            #     print(sheet_name + " Sheet Skipped")
            #     continue

            # Skip extra sheets , setup header
            if(self.should_skip_sheet(sheet_name)):
                self.log.debug(sheet_name + " Sheet Skipped")
                continue

            # print(f"sheet_index {sheet_index}")

            header = self.header[sheet_index]
            _row = dict()
            # print(header)
            # print(data)
            # print()
            # print()
            self.header_less_row(data, header)  # fix for header less sheets

            """
            Convert list to dicts
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
                ('RRC-4SP', '19" RACK CASE, 4U SPACE',
                 761294218389.0, 249.99, 156.25),
                ('PSB-7U', 'AC ADAPTOR (Order as Part #5100047496 this includes AC cord)',
                 5100047496.0, 40.11, 28.65),
                ...
            }
            """
            rows = zip(*data["table_data"])

            # if(sheet_index == 1):
            #     print(list(rows))
            #     exit()
            """
                Loop through rows
                prepare new row with required format
                and append in new variable `csv_rows`
            """
            category = ""
            for row_index, row in enumerate(rows):
                _row = dict()

                """
                print(any([2 == 2, 3 == 2]))    => True
                print(any([True, False, False]))    => True
                print(any([False, False])) => False
                """
                # if sheet_index != 2:
                #     continue
                #     print(row)
                #     print(self.all_sheet_headers)
                #     exit()

                if any(row):

                    # Skip if header column name
                    # header row detected  ('Item Name', 'Item Code', 'List', 'Dealer', 'Weight', 'Length', 'Width', 'Height')

                    # header_col_name_found = False
                    # for row_text in row:
                    #     if (str(row_text).lower() in self.all_sheet_headers):
                    #         header_col_name_found = True
                    #         break
                    if(self.is_header_col(row)):
                        self.log.debug("header row detected " + str(row))
                        continue

                    # All indexes we have
                    # self.all_sheet_headers index
                    # self.header[sheet_index] index
                    # list(row) index
                    non_empty_col_data = []
                    for h_index, h_text in enumerate(self.all_sheet_headers):
                        if h_text not in ["ext_category", "sheet_name"]:
                            for m_sheet_index, m_val in enumerate(self.header_vs_all_mapping[h_index]):
                                if m_sheet_index == sheet_index:
                                    if m_val > -1:  # and len(row) > m_val:
                                        try:
                                            col_val = row[m_val]
                                        except IndexError:
                                            print(
                                                f"IndexError Sheet {m_sheet_index} - Row[{row_index}][{m_val}]")
                                            # print(f"sheet_index = {sheet_index} h_index {h_index} - h_text {h_text}")
                                            # print(row)
                                            # print(self.header_vs_all_mapping[h_index])
                                            # print(self.all_sheet_headers)
                                            # exit()

                                        if col_val:
                                            non_empty_col_data.append(col_val)
                                    else:
                                        col_val = ""  # f"{h_index}"

                                    if(col_val):
                                        _row.update({h_text: col_val})

                    # add sheet name as extra field
                    # and uppend row to csv  row

                    _row.update({"sheet_name": sheet_name})
                    # print(non_empty_col_data)
                    if len(non_empty_col_data) == 1:
                        category = non_empty_col_data.pop()
                        # continue
                        # print(category)
                        # exit()

                    if category:
                        _row.update({"ext_category": category})
                    else:
                        _row.update({"ext_category": ""})

                    all_row_empty = all(
                        element == "" for element in list(_row.values()))
                    if (not all_row_empty):
                        self.csv_rows.append(_row)

                else:
                    None
                    # print(row , "All empty")

                # print(row)
                # print(self.csv_rows)
                # exit()

    # Write to csv
    def write(self):

        # print(csvfilepath)
        with open(self.dest_csv_path, 'w', encoding='UTF8', newline='') as f:
            # writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer = csv.DictWriter(f, fieldnames=self.all_sheet_headers)
            writer.writeheader()

            # print(self.all_sheet_headers)
            writer.writerows(self.csv_rows)
            # i = 1

            # for key_val in self.csv_rows:
            #     print("---")
            #     print(key_val)
            #     i = i + 1
            #     if (i > 10 ):
            #         break

            # for curr_row in self.csv_rows:
            #     for all_h_key in self.all_sheet_headers:
            #         if(all_h_key in curr_row.keys()):
            #             if(curr_row.get(all_h_key,"")):
            #                 writer.writerow({all_h_key: curr_row.get(all_h_key,"")})
            # prepare row first and then write

            # print(key_val)
            # print(all_h_key)
            # print(key_val.get(all_h_key,""))
            # print(all_h_key in key_val.keys())
            # exit()
            # if (all_h_key in key_val.keys()):
            #     # for key , val in key_val.items():
            #     writer.writerow(key_val)


if __name__ == '__main__':
    # argument for souce filename
    # argument for destination filename
    source_xls_path = sys.argv[1]
    dest_csv_path = sys.argv[2]
    # print(source_xls_path)
    # print(dest_csv_path)

    # xlsObj = XlsToCsv('test_excel.xlsx')
    xlsObj = XlsToCsv(source_xls_path, dest_csv_path)

    # print(xlsObj.source_xls_path)
    # print(xlsObj.dest_csv_path)

    # $ py ./xls_to_csv.py ./excel/AVR\ Pricelist\ -\ Roland\ Pro\ AV\ Jan\ 24th\ 2022.xlsm ./csv/AVR\ Pricelist\ -\ Roland\ Pro\ AV\ Jan\ 24th\ 2022.csv
    # $ py ./xls_to_csv.py ./excel/AVR\ Pricelist\ -\ Roland\ Pro\ AV\ Jan\ 24th\ 2022.xlsm ./csv/AVR\ Pricelist\ -\ Roland\ Pro\ AV\ Jan\ 24th\ 2022.csv
    # exit()

    # xlsObj = XlsToCsv('Harman Pro Pricing 010522.xlsx')
    # xlsObj = XlsToCsv("EAW Dealer Price List April 2022.xlsx")
    # xlsObj = XlsToCsv("DMR Price List 1-1-2022.xlsx")
    # xlsObj = XlsToCsv("AVR Pricelist - Roland Pro AV Jan 24th 2022.xlsm")
    # xlsObj = XlsToCsv("Visionary Solutions - Dealer Price List - Effective Feb 15 2022.xlsx")
    xlsObj.parsed_excel()
    xlsObj.prepare_csv_rows()
    xlsObj.write()
    logging = Log()
    logging.info("CSV conversion done!")

    if(xlsObj.response):
        print(json.dumps(xlsObj.response))
    else:        
        xlsObj.response["status"] = "success"
        xlsObj.response["message"] = "CSV conversion done!"
        print(json.dumps(xlsObj.response))

    # print (xlsObj.csvfilepath[0])

    # db = DB()
    # print(xlsObj.csvfilepath[0])
    # db.insert(title="test_excel",columns=xlsObj.header,csvpath=os.path.normpath(xlsObj.csvfilepath[0]))
