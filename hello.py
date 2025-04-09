import mysql.connector
import os
from prettytable import PrettyTable

from dotenv import load_dotenv

load_dotenv()

cnx = mysql.connector.connect(user = 'ruz',
                               host = 'localhost',
                              password=os.getenv("MYSQL_PASS") ,
                              database='db',
                              ssl_disabled=True)

c = cnx.cursor()


def pretty_print_mysql(out):
    
    print(out)

    if out.with_rows:  # Only fetch results for SELECT queries

        table = PrettyTable()

        table.field_names = [ i[0] for i in c.description ]

        for row in out:
            table.add_row(row)

        print( table )
    else:
        print("no output")

    print("")
    
def mysql_run_and_pretty_print(commands):
    for out in c.execute(commands , multi=True):
        pretty_print_mysql(out)
 
    
mysql_run_and_pretty_print("""
use db;
CREATE TABLE likes (     id INT PRIMARY KEY AUTO_INCREMENT,     user_id INT,     post_id INT,     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,     FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE );

""")

cnx.commit()
cnx.close()
