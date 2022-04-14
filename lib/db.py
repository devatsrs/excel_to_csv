from asyncio import subprocess
from asyncio.windows_utils import Popen
import os
import mysql.connector

class DB():

    def __init__(self):
        self.cnx = mysql.connector.connect(
                        host="127.0.0.1",
                        port=3307,
                        user="root",
                        password="root",
                        database='pricedonkey_db_dev'
                        )

    def close(self):
        # Close connection
        self.cnx.close()

    def test(self):
        cur = self.cnx.cursor()
        # Execute a query
        cur.execute("SELECT CURDATE()")
        # Fetch one result
        row = cur.fetchone()
        print("Current date is: {0}".format(row[0]))
        cur.close()
        self.cnx.commit()

        self.close()

    def insert(self, title, columns , csvpath):
        
        # INSERT INTO WPDATATABLE
        # Get a cursor
        cur = self.cnx.cursor()
        sql = f"""INSERT INTO
                `wp_7_wpdatatables` (
                    `title`,`show_title`,`table_type`,`connection`,`content`,`filtering`,`filtering_form`,`sorting`,`tools`,`server_side`,`editable`,`inline_editing`,`popover_tools`,`editor_roles`,`mysql_table_name`,`edit_only_own_rows`,`userid_column_id`,`display_length`,`auto_refresh`,`fixed_columns`,`fixed_layout`,`responsive`,`scrollable`,`word_wrap`,`hide_before_load`,`var1`,`var2`,`var3`,`tabletools_config`,`advanced_settings` )
                VALUES
                (
                    '{title}','1','manual','','SELECT * FROM wp_7_wpdatatable_pkid',1,0,1,1,1,0,0,0,'','wp_7_wpdatatable_pkid',0,0,10,0,1,0,0,0,0,0,'','','','',''
                );"""

        # Execute a query

        # print(sql)
        cur.execute(sql)
        siteid = 7
        tablename = f"wp_{siteid}_wpdatatable_{cur.lastrowid}"
        wpdatatables = f"wp_{siteid}_wpdatatables"
        sql = f""" UPDATE {wpdatatables} SET
                     content = 'SELECT * FROM {tablename}',
                     mysql_table_name = '{tablename}'
                    WHERE id = {cur.lastrowid};
                """
        # print(sql)
        cur.execute(sql)
        # Make sure data is committed to the database
        # print("data inserted")
        
        # csvsql --delimiter ',' --db mysql://root:root@localhost:3307/pricedonkey_db_dev ./csv/test_excel.csv --insert --create-if-not-exists --tables wp_7_wpdatatable_123 
        # csvsql --db mysql://root:root@localhost:3307/pricedonkey_db_dev ./csv/test_excel.csv  --create-if-not-exists --tables wp_7_wpdatatable_123 
        # insert data 

        csvpath=csvpath.replace("\\","//")

        # csvsql --delimiter ',' --db mysql://root:root@localhost:3307/pricedonkey_db_dev ./csv/test_excel.csv  --tables wp_7_wpdatatable_59
        command = f" --delimiter , --db mysql://root:root@localhost:3307/pricedonkey_db_dev {csvpath} --tables {tablename}"
        # print(command)
        os.system("csvsql " + command)
        # with Popen(["csvsql",command], stdout=subprocess.PIPE) as proc:
        #    print(proc.stdout.read())
        #    print("command run successfully...")


        command = f"--delimiter , --db mysql://root:root@localhost:3307/pricedonkey_db_dev {csvpath} --insert --create-if-not-exists --tables {tablename} --prefix IGNORE "
        # print(command)
        os.system("csvsql "+ command)
        # with Popen(["csvsql",command], stdout=subprocess.PIPE) as proc:
        #    print(proc.stdout.read())
        #    print("command run successfully...")
        #    #    sql = (proc.stdout.read())
        #    #cur.execute(sql)


        # insert primary key
        sql = f"""ALTER TABLE `{tablename}`
                    ADD COLUMN `wdt_ID` INT(11) NOT NULL AUTO_INCREMENT FIRST,
                    ADD PRIMARY KEY (`wdt_ID`);
            );
            """
        # print(sql)
        cur.execute(sql)
        self.close()


