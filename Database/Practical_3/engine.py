from cgi import print_arguments
from operator import index
from os import sep
import time

from simple_db import SimpleDatabase
import sqlite3

# def print_selected(header, rows):
#     # header is a list of column names, rows is a list of rows
#     # in turn, each row is a list of column values
#     # e.g., if header = ['student name', 'ID', 'mark']
#     # join command below will result in "student name, ID, mark"
#     print('_' * 30) # repeat symbol '_' 30 times, thus creating a printed 'line'
#     print(', '.join(header))
#     print('_' * 30)
#     for row in rows:
#         print(', '.join(row))
#     print('_' * 30)



# a little improve    
def print_selected(header, rows):
    line = '+' + '-' * 30
    print(line * 4, '+', sep = '')
    
    # get the length of header & rows (list)
    header_length = len(header)
    
    # print header
    for i in range(header_length):   
        print('|' + header[i].center(30), end='')
    print('|', sep='')
    
    
    print(line * 4, '+', sep = '')
    
    # print rows
    for row in rows:
        print('|', end='')
        for i in range(header_length):
            print(row[i].center(30) + '|', end= '', sep = '')
        print()
    # print(sep='')
    
        
    print(line * 4, '+', sep = '')
    
    
def print_tables(names):
    line = '+' + '-' * 30
    print(line, '+', sep = '')
    print('|' + 'Tables & Indexes'.center(30) + '|')
    print(line, '+', sep = '')
    
    # get the length of the name (list)
    length = len(names)
    
    for i in range(length):
        print('|' + names[i].center(30), '|', sep = '')
    
    print(line, '+', sep = '')


def run_engine():
    print("Welcome to our Database Management System (⸝⸝•‧̫•⸝⸝)")  
    # print("Notice that commands should end with ; symbol.")
    print("Type 'help;' to enter our Help Center.")
    print()
    db = SimpleDatabase()
    
    while True:
        command = input("Enter command: ")
        if not command.endswith(";"):
            print("Tips: Commands should end with ; symbol.")
            print()
            continue

        command = command[:-1]  # to remove ; from the end
        if command == "exit":
            print("Leaving, bye ૮ ・ﻌ・ა ")
            print()
            # print("¨̮ ᴴᴬᵛᴱ ᴬ ᴳᴼᴼᴰ ᵀᴵᴹᴱ દ ᵕ̈ ૩")
            break
        
        elif command == "help":
            print()
            print("Welcome to our Help Center *⸜( •ᴗ• )⸝*")
            print('''
                へ　　　　　／|
            　　/＼7　　　 ∠＿/
            　 /　│　　 ／　／
            　│　Z ＿,＜　／　　 /`ヽ
            　│　　　　　ヽ　　 /　　〉
            　 Y　　　　　`　 /　　/
            　ｲ●　､　●　　⊂⊃〈　　/
            　()　 へ　　　　|　＼〈
            　　>ｰ ､_　 ィ　 │ ／／
            　 / へ　　 /　ﾉ＜| ＼＼
            　 ヽ_ﾉ　　(_／　 │／／
            　　7　　　　　　　|／
            　　＞―r￣￣`ｰ―＿
                  ''')
            print("Here are the commands you can use:")
            print()
            print("                            Commands                                                          Descriptions                                    ")   
            print("1.   show tables                                                               --> show all tables & indexes in the database")
            print("2.   copy <table_name> to <file_name>                                          --> copies table to a file")
            print("3.   select <column_name> from <table_name> where <column_name> = <value>      --> selects rows from table")
            print("4.   create index <column_name> on <table_name>                                --> creates index on a column")
            print("5.   drop index <column_name> on <table_name>                                  --> drops index on a column")
            print("6.   exit                                                                      --> exit the database")
            print()
            print("Tips: Do not forget that commands should end with ; symbol.")
            
            
        elif command == "show tables":
            # modify this section, so that the command
            # also prints columns for which index was built
            # note that our DBMS only supports loading one table at a time
            name = []
            table_name = db.get_table_name()
            if table_name is None:
                print("... no tables loaded ...")
                print("Tips: use 'copy <table_name> to <file_name>' to load a table")
            else:
                index_names = db.get_index_name()            # get index name (list)
                name.append(table_name)
                for i in index_names:
                    i = 'Index on column ' + i
                    name.append(i)
                print_tables(name)
    
            
        elif command.startswith("copy "):
            # e.g., copy my_table from 'file_name.csv'
            words = command.split() # breaks down command into words
            # words[0] should be copy, words[1] should be table name, etc.
            if len(words) != 4:
                # we expect a particular number of words in this command
                print("Incorrect command format")
                continue

            table_name = words[1]
            file_name = words[3][1:-1] # to remove ' around file name
            db.load_table(table_name, file_name)
            
        elif command.startswith("select * from "):
            # e.g., select * from my_table where name="Bob"
            command = command.replace("=", " = ") # ensure spaces around =
            words = command.split() # breaks down command into words
            if len(words) != 8:
                # we expect a particular number of words in this command
                print("Incorrect command format")
                continue
            
            table_name = words[3]
            column_name = words[5]
            column_value = words[7][1:-1] # to remove " around the value
            
            start = time.time()
            if db.index_exists(column_name):
                header, rows = db.select_index(column_name, column_value)
            else:
                header, rows = db.select_rows(table_name, column_name, column_value)
            end = time.time()
            
            if len(header) == 0:
                print("... no such table ...")
            else:
                print_selected(header, rows)
                print("Time elapsed: ", round(1000*(end - start)), " ms")

        
        # add code for processing create index and drop index here ...
        # create index
        elif command.startswith("create index on "):
            # e.g., create index on column_name
            words = command.split()
            
            # get the column name
            col_name = words[-1]
            
            # check if the column name is valid
            if col_name not in db.get_table_header():
                print("Error: wrong column name")
                
            # check if the index already exists
            elif col_name in db.get_index_name():
                print("Error: index already exists")    
                
            # create the index
            else:
                db.create_index(col_name)
                print("Created index for", col_name)
        
        # drop index
        elif command.startswith("drop index on "):
            # e.g., drop index on column_name
            words = command.split()
            
            # get the column name
            col_name = words[-1]
            
            # check if the column name is valid
            if col_name not in db.get_table_header():
                print("Error: wrong column name")
                
            # check if the index is valid
            elif col_name not in db.get_index_name():
                print("Error: index does not exist")
            
            # drop the index
            else:
                db.drop_index(col_name)
                print("Dropped index for", col_name)    
            
        else:
            print("Unrecognized command!")

        print() # empty line after each command


if __name__ == "__main__":
    run_engine()
    
    
# Command:    
# copy students from 'students_large.csv';
# select * from students where grade="D";
# select * from students where id="a61370565";
# create index on id;
# create index on grade;
# show tables;
# drop index on id;