# Inroduction

    This project is make from https://github.com/gristlabs/grist-core to

# excel_to_csv

export PATH="$HOME/.local/bin:$PATH"

# Setup

sudo apt-get install python3-venv
python3 -m venv venv
sudo chown -R bitnami:daemon /opt/bitnami/apache/htdocs
sudo chmod -R 775 /opt/bitnami/apache/htdocs
sudo -u daemon /opt/bitnami/apache/htdocs/excel_to_csv/venv/bin/python3 /opt/bitnami/apache/htdocs/excel_to_csv/venv/bin/pip3 install -r requirements.txt

# Test

sudo -u daemon /opt/bitnami/apache/htdocs/excel_to_csv/venv/bin/python3 /opt/bitnami/apache/htdocs/excel_to_csv/xls_to_csv.py /opt/bitnami/apache/htdocs/wp-content/uploads/sites/7/2022/04/DMR-Price-List-1-1-2022.xlsx /opt/bitnami/apache/htdocs/wp-content/uploads/sites/7/2022/04/DMR-Price-List-1-1-2022.csv

# Execute

python ./xls_to_csv.py [souce_excel_path] [destination_csv_path]

python ./xls_to_csv.py 'D:\laragon\www\gkb_req\pricedonkey\pythontest\excel\test_excel.xlsx' 'D:\laragon\www\gkb_req\pricedonkey\pythontest\csv\test_excel.csv'
