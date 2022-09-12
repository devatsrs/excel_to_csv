# Inroduction

This project is made from https://github.com/gristlabs/grist-core with add on following requirements.

# Challenges & Our Approach 

## Challenges

    1. Convert Excel to CSV
    2. Identify Headers 
    3. Identify Category 
    4. Identify Sheets to be import
    5. Duplicate Column Name
    6. Parallel Tables
    7. Blank Header Title 

## Our Approach 

    1. Python Messytable library
    2. Python Messytable library
    3. Custom Logic - Heading like text above group of price list with rest columns empty
    4. Custom Logic - Manually added skip list 
    5. Rename with post fix _1 ie "dealer price_1"
    6. We applies same rule no #5
    7. Blank Header will replace ie "__1__"



# excel_to_csv

export PATH="$HOME/.local/bin:$PATH"

# Setup

sudo apt-get install python3-venv

python3 -m venv venv

sudo chown -R bitnami:daemon /opt/bitnami/apache/htdocs

sudo chmod -R 775 /opt/bitnami/apache/htdocs

sudo -u daemon /opt/bitnami/apache/htdocs/excel_to_csv/venv/bin/python3 /opt/bitnami/apache/htdocs/excel_to_csv/venv/bin/pip3 install -r requirements.txt

# Test

sudo -u daemon /opt/bitnami/apache/htdocs/excel_to_csv/venv/bin/python3 /opt/bitnami/apache/htdocs/excel_to_csv/xls_to_csv.py /opt/bitnami/apache/htdocs/wp-
content/uploads/sites/7/2022/04/DMR-Price-List-1-1-2022.xlsx /opt/bitnami/apache/htdocs/wp-content/uploads/sites/7/2022/04/DMR-Price-List-1-1-2022.csv

# Unit test 

    python -m unittest -v runtests/test_import_xls.py
    python -m unittest discover -s  runtests/ -v    
    
# Execute

python ./xls_to_csv.py [souce_excel_path] [destination_csv_path]

python ./xls_to_csv.py ./excel/test_excel.xlsx ./csv/test_excel.csv
python ./xls_to_csv.py 'D:\laragon\www\gkb_req\pricedonkey\pythontest\excel\test_excel.xlsx' 'D:\laragon\www\gkb_req\pricedonkey\pythontest\csv\test_excel.csv'

# Todo

    pdf process with messytables
    https://messytables.readthedocs.io/_/downloads/en/stable/pdf/

# Reference

    https://towardsdatascience.com/how-to-work-with-excel-files-in-pandas-c584abb67bfb#:~:text=To%20tell%20pandas%20to%20start,number%20of%20rows%20to%20skip.

# Col match tool

    python -W ignore col_match.py desc Products,Descriptions,MSRP,Dealer%20Price,MAP%20Price