import calendar
import datetime
import math
import os
import unittest
import xls_to_csv
from collections import Counter


class TestExcelImportXLS(unittest.TestCase):

    def __init(self):
        self.result_rows = []
        self.result_headers = []

    def _get_fixture(self, filename):
        return [os.path.join(os.path.dirname(__file__), "../excel", filename), filename]

    def _check_col(self, sheet, index, name, typename, values):
        self.assertEqual(sheet["column_metadata"][index]["id"], name)
        self.assertEqual(sheet["column_metadata"][index]["type"], typename)
        if typename == "Any":
            # Convert values to strings to reduce changes to tests after imports were overhauled.
            values = [str(v) for v in values]
        self.assertEqual(sheet["table_data"][index], values)

    def _parse_file(self, source_file_path):
        source_xls_path, xls_filename = self._get_fixture(source_file_path)
        dest_csv_path, csv_filename = self._get_fixture('test.csv')
        xlsObj = xls_to_csv.XlsToCsv(source_xls_path, dest_csv_path)
        xlsObj.convert_n_load_parsed_data()
        xlsObj.prepare_csv_rows()
        self.result_rows = xlsObj.csv_rows
        self.result_headers = xlsObj.all_sheet_headers
        # return [xlsObj.csv_rows, xlsObj.all_sheet_headers]

    def _setup_file(self):
        self._parse_file("../excel/test_excel.xlsx")

        # self.assertEqual(len(rows), 16)
    def test_header(self):
        self._setup_file()
        expected_header = ["sku", "category", "model number", "status", "product description long", "msrp", "map", "dealer", "master pack qty", "upc", "ean",
                           "weight (lb.)", "dim l (in.)", "dim w (in.)", "dim h (in.)", "country of origin", "taa compliant", "link", "taa compliance", "sheet_name", "ext_category"]

        # compare header
        self.assertListEqual(self.result_headers, expected_header)

        # self.assertEqual(len(rows), 16)

    def test_rows(self):
        self._setup_file()
        # no of rows
        self.assertEqual(len(self.result_rows), 18)

    def test_sheet_name(self):
        self._setup_file()
        # no of rows
        SheetName = Counter()
        for row in self.result_rows:
            SheetName[row["sheet_name"]] = SheetName[row["sheet_name"]] + 1
            # print(row["sheet_name"])

        # print(SheetName)        Counter({'AKG': 5, 'DBX': 5, 'AMX': 3, 'BSS': 3, 'Crown': 2})
        self.assertEqual(SheetName['AMX'], 3)
        self.assertEqual(SheetName["AKG"], 5)
        self.assertEqual(SheetName["BSS"], 3)
        self.assertEqual(SheetName["Crown"], 2)
        self.assertEqual(SheetName["DBX"], 5)

    def test_ext_category(self):
        self._setup_file()
        # no of rows
        SheetName = Counter()
        for row in self.result_rows:
            category = row["ext_category"].strip()
            SheetName[category] = SheetName[category] + 1
            # print(row["sheet_name"])

        # print(SheetName)        Counter({'AKG': 5, 'DBX': 5, 'AMX': 3, 'BSS': 3, 'Crown': 2})
        self.assertEqual(SheetName['Wired Microphones-Recording'], 1)
        self.assertEqual(SheetName["USB"], 4)


if __name__ == '__main__':
    unittest.main()
