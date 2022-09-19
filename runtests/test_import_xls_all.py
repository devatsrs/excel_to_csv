import shutil
import  subprocess
import calendar
import datetime
import json
import math
import os
import re
import time
import unittest
import xls_to_csv
from collections import Counter


class TestExcelImportXLSAll(unittest.TestCase):

    
    def run_command_sync(self,cmd):
        """
        Run a command using the synchronous `subprocess.run`.
        The asynchronous `run_command_async` should be preferred,
        but does not work on Windows, so use this as a fallback.

        Parameters
        ----------
        iterable
            An iterable of command-line arguments to run in the subprocess.

        Returns
        -------
        A tuple containing the (return code, stdout)
        """
        try:
            process = subprocess.run(cmd, stdout=subprocess.PIPE,shell=True, check=True,capture_output=True)
        except subprocess.CalledProcessError as err:
            pass
        code = process.returncode
        out = process.stdout.decode('utf-8')
        return (code, out) 

    def test_run_all_excel(self):

        # folder path
        dir_path = r'D:\\laragon\\www\\excel_to_csv\\excel\\'

        # Iterate directory
        for xls_path in os.listdir(dir_path):
            # check if current path is a file
            if ( xls_path != ".gitkeep" and os.path.isfile(os.path.join(dir_path, xls_path)) ):
                # res.append(path)
                # print("Path : " ,xls_path)
                xls_ext = os.path.splitext(xls_path)[1]
                xls_path_ = (re.escape(xls_path)).replace("\.",".")
                # xls_path = xls_path.replace(" ","\ ")
                # print("xls_path : " ,xls_path)
                csv_path = xls_path.replace(xls_ext,".csv")
                command = '"./venv/Scripts/python.exe" ./xls_to_csv.py "./excel/%s" "./csv2/%s"' % (xls_path, csv_path)
                # code , output = self.run_command_sync(command)

                # shutil.copyfile("./excel/"+xls_path, "./xls/"+ xls_path.replace(" ","_"))
                # print("./excel/"+xls_path, " -> ./xls/"+ xls_path.replace(" ","_"))

                print(command)
                output = subprocess.getoutput(command)
                print(f"output = {output} ")
                # time.sleep(5)
                result = json.loads(output)
                # print(result)
                
                if(result["status"] !="success"):
                    print("CSV Failed")
                    print(command)
                    print(output)

                # ./excel/B-Tech AV Mounts LLC Price List 2021 (Release 1.0) - Sapphire Partner.xlsx
                # ./excel/B-Tech\ AV\ Mounts\ LLC\ Price\ List\ 2021\ \(Release\ 1.0\)\ -\ Sapphire\ Partner.xlsx
                # ./excel/B\-Tech\ AV\ Mounts\ LLC\ Price\ List\ 2021\ \(Release\ 1.0\)\ \-\ Sapphire\ Partner.xlsx 

if __name__ == '__main__':
    unittest.main()
