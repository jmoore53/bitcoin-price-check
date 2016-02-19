import MySQLdb

'''

Python Script to create an sql database for the RealTime_Bitcoin_Values_Script.py

'''
#Script that creates a mysql database

def create_database():
    connection = MySQLdb.connect(host = "localhost", user = "root", passwd="sqlpassword", db = "bitcoin")
    #raspberrypi password= sqlpassword
    #raspberrypi needs parameter '(passwd="sqlpassword")'
    cursor = connection.cursor()
    global sql1, sql2
    try: 
##        cursor.execute("""
##                        CREATE DATABASE IF NOT EXISTS
##                        `bitcoin` DEFAULT CHARACTER
##                        SET latin1 COLLATE latin1_swedish_ci;
##                        """)
        cursor.execute('USE bitcoin')
##        cursor.execute("""
##                        CREATE TABLE IF NOT EXISTS time_and_rates (
##                          `Time` datetime NOT NULL,
##                          `ExchangeRate` float(10,2) NOT NULL
##                        ) ENGINE=CSV DEFAULT CHARSET=latin1;
##                        """)
##        cursor.execute("""CREATE TABLE IF NOT EXISTS `error_log` ( `Error` TINYTEXT NOT NULL , `Exception Time` DATETIME NOT NULL ) ENGINE = CSV;
##            """)
##        cursor.execute("""
##                        ALTER TABLE `error_log` CHANGE `Error` `Error` TINYTEXT CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
##                        """)
##        a = cursor.execute("""SELECT * FROM `error_log`""")
##This prints a database to a file in the temporary folder
        cursor.execute("""SELECT * FROM time_and_rates INTO OUTFILE '/tmp/temp_database.txt' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';""")
        connection.commit()
        connection.close()
        print("Database accessed successfully!")
    except Exception as e:
        #connection.rollback()
        print("Database is rolling back")
        print(e)

create_database()
