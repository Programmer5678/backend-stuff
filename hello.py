import mysql.connector
from prettytable import PrettyTable

cnx = mysql.connector.connect(user = 'ruz',
                               host = 'localhost',
                              password= 'p123',
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
select * from posts;
""")

cnx.commit()
cnx.close()
