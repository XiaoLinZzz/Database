class help_center:
    def help():
        print("Welcome to our Help Center  *⸜( •ᴗ• )⸝*")
        print("We will help you make better use of our database.")
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
        
        # command
        print("Here are the commands you can use:")
        print('''
                                        Commands                                                                Descriptions                                 
            1.   show tables                                                               -->       show all tables & indexes in the database
            2.   copy <table_name> to <file_name>                                          -->       copies table to a file
            3.   select * from <table_name> where <column_name> = <value>                  -->       selects rows from table
            4.   create index <column_name> on <table_name>                                -->       creates index on a column
            5.   drop index <column_name> on <table_name>                                  -->       drops index on a column
            6.   exit                                                                      -->       exit the database
              
              ''')
        print()
        
        # Errors & Tips
        print("Our database can detect the following errors and give you hints.")
        print('''
            1.   Command without ; symbol                                                  -->       Error: Commands should end with ; symbol.
            2.   When table is empty                                                       -->       Error: No tables loaded       
                                                                                                     Tips:  Use 'copy <table_name> to <file_name>' to load a table.
            3.   If you entered the column are not exist                                   -->       Error: Wrong column name.
            4.   If you entered the table are not exist                                    -->       Error: No such table.
            5.   If you want to create the index which is already exits                    -->       Error: Index already exists.
            6.   If you want to drop the index which is not exits                          -->       Error: Index does not exist.
            7.   We will dectect the format when you use 'select' and 'copy' command       -->       Error: Incorrect command format.
            8.   General command error                                                     -->       Error: Unrecognized command!
              
              ''')
        
        print("Tips: Do not forget that commands should end with ; symbol.")