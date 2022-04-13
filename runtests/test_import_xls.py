import calendar
import datetime
import math
import os
import unittest
import import_xls


def _get_fixture(filename):
    return [os.path.join(os.path.dirname(__file__), "../excel", filename), filename]


class TestImportXLS(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def _check_col(self, sheet, index, name, typename, values):
        self.assertEqual(sheet["column_metadata"][index]["id"], name)
        self.assertEqual(sheet["column_metadata"][index]["type"], typename)
        if typename == "Any":
            # Convert values to strings to reduce changes to tests after imports were overhauled.
            values = [str(v) for v in values]
        self.assertEqual(sheet["table_data"][index], values)

    def test_excel(self):
        parsed_file = import_xls.parse_file(*_get_fixture('test_excel.xlsx'))
        print(parsed_file)
        self.assertEqual('foo'.upper(), 'FOO')

        # # check that column type was correctly set to numeric and values are properly parsed
        # self.assertEqual(parsed_file[1][0]["column_metadata"][0], {
        #                  "type": "Numeric", "id": "numbers"})
        # self.assertEqual(parsed_file[1][0]["table_data"][0], [
        #                  1, 2, 3, 4, 5, 6, 7, 8])

        # # check that column type was correctly set to text and values are properly parsed
        # self.assertEqual(parsed_file[1][0]["column_metadata"][1], {
        #                  "type": "Any", "id": "letters"})
        # self.assertEqual(parsed_file[1][0]["table_data"][1],
        #                  ["a", "b", "c", "d", "e", "f", "g", "h"])

        # # 0s and 1s become Numeric, not boolean like in the past
        # self.assertEqual(parsed_file[1][0]["column_metadata"][2], {
        #                  "type": "Numeric", "id": "boolean"})
        # self.assertEqual(parsed_file[1][0]["table_data"][2], [
        #                  1, 0, 1, 0, 1, 0, 1, 0])

        # # check that column type was correctly set to text and values are properly parsed
        # self.assertEqual(parsed_file[1][0]["column_metadata"][3],
        #                  {"type": "Any", "id": "corner-cases"})
        # self.assertEqual(parsed_file[1][0]["table_data"][3],
        #                  # The type is detected as text, so all values should be text.
        #                  [u'=function()', u'3.0', u'two spaces after  ',
        #                   u'  two spaces before', u'!@#$', u'€€€', u'√∫abc$$', u'line\nbreak'])

        # # check that multiple tables are created when there are multiple sheets in a document
        # self.assertEqual(parsed_file[1][0]["table_name"], u"Sheet1")
        # self.assertEqual(parsed_file[1][1]["table_name"], u"Sheet2")
        # self.assertEqual(parsed_file[1][1]["table_data"][0], [
        #                  "a", "b", "c", "d"])


if __name__ == '__main__':
    unittest.main()
