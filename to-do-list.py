import sys
import argparse
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
    
def print_items():
    for (id, item, finished) in c.fetchall():
        print("id: ", id, ", item: ", item, ", finished? ", "yes" if finished else "no" )
        
def validateId(id):
    
    c.execute(f"select id from to_do_list where id={id};")

    if not c.fetchall():
        raise argparse.ArgumentTypeError("FUCK")
        
    return id
        
    
# c.execute("""
# create trigger my_trigger_not_nigga
# before insert on t
# for each row
# begin
# insert into ttt values(new.a );
# end
# """)    
    
# mysql_run_and_pretty_print("""
# use db;
 
# describe t;
# select * from t;

# select * from ttt;

# """)

parser = argparse.ArgumentParser(description="""This is passed a description into the argument parser, but i wouldnt say that is accurate.
                                 it is the help message. """)

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--new", "-n", help="add a new todo item")
group.add_argument("--list", "-l", help="list todo items", choices=["all", "pending", "done"])
group.add_argument("--delete", "--del", help="delete a todo item", type=validateId)
group.add_argument("--done", help="mark a todo item as done",  type=validateId)
group.add_argument("--version", action="store_true" , help="to print the version of the application")

args = parser.parse_args()
    
# mysql_run_and_pretty_print("""
                                                      
# describe to_do_list;
# show create table to_do_list;
# select * from to_do_list;

# """)
    
# print("parser: ", parser, "\ngroup: ", group, "\nargs: ", args, "\nargs.list: ", args.list, "\nargs.new: ", args.new)

if args.new: 
    c.execute(f"insert into to_do_list (item) values ('{args.new}') ;")
    print(f"adding \'{args.new}\' to to-do-list. Run -l to confirm")
    
if args.list:
    
    if args.list == 'all':
        c.execute("select * from to_do_list;")
        print_items()
        
        
    elif args.list == 'pending':
        c.execute("select * from to_do_list where finished=0;")
        print_items()
        
    elif args.list == 'done':
        c.execute("select * from to_do_list where finished=1;")
        print_items()
        
        
if args.delete:
    c.execute(f"select id, item from to_do_list where id={args.delete};")
    stuff = c.fetchall()
    
    # add error check for when id is invalid
    c.execute(f"delete from to_do_list where id={args.delete};")
    print(f"deleting '{stuff[0][1]}' from to-do-list( item with id {stuff[0][0]} ) ")



if args.done:
    c.execute(f"select * from to_do_list where id={args.done};")
    stuff = c.fetchall()
    
    # add error check for when id is invalid
    c.execute(f"update to_do_list set finished=1 where id={args.done};")
    
    if stuff[0][2]:
        print(f"'{stuff[0][1]}' from to-do-list already marked as done( item with id {stuff[0][0]} ) ")
        
    else:
        print(f"marking '{stuff[0][1]}' from to-do-list as done( item with id {stuff[0][0]} ) ")
    
    
if args.version:
    print(f"version 2.5 ya shit")
    
    
cnx.commit()
cnx.close()
