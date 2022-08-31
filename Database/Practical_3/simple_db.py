
# from distutils.log import error
# from msilib.schema import tables
import os

from b_tree import BTree


class SimpleDatabase:
    def __init__(self):
        # before an actual table is loaded, class members are set to None
        
        # a header is a list of column names
        # e.g., ['name', 'id', 'grade']
        self.header = None
        
        # map column name to column index in the header
        self.columns = None
        
        # None if table is not loaded
        # otherwise list b-tree indices corresponding to columns 
        self.b_trees = None

        # rows contains actual data; this is a list of lists
        # specifically, this is a list of rows, where each row
        # is a list of values for each column
        # e.g., if a table with the above header has two rows
        # self.rows can be [['Alice', 'a1234', 'HD'], ['Bob', 'a7654', 'D']]
        self.rows = None

        # name of the loaded table
        self.table_name = None
        
        # record the index name
        # self.index_names = None

    def get_table_name(self):
        return self.table_name

    def load_table(self, table_name, file_name):
        # note our DBMS only supports loading one table at a time
        # as we load new table, the old one will be lost
        print(f"Loading {table_name} from {file_name} ...")

        if not os.path.isfile(file_name):
            print("File not found")
            return

        # note, you could use a CSV module here, also we don't check
        # correctness of file
        with open(file_name) as f:
            self.header = f.readline().rstrip().split(",")
            self.rows = [line.rstrip().split(",") for line in f]
        self.table_name = table_name
        
        self.columns = {}
        for i, column_name in enumerate(self.header):
            self.columns[column_name] = i
            
        self.b_trees = [None] * len(self.header)
        print("Successfully loaded. Enjoy your query (ᕑᗢᓫ∗)")

    def select_rows(self, table_name, column_name, column_value):
        # modify this code such that row selection uses index if it exists
        # note that our DBMS only supports loading one table at a time
        if table_name != self.table_name:
            # no such table
            return [], []

        if column_name not in self.columns:
            # no such column
            return self.header, []
            
        col_id = self.columns[column_name]
        
        selected_rows = []
        for row in self.rows:
            if row[col_id] == column_value:
                selected_rows.append(row)
        
        return self.header, selected_rows
    
    def select_index(self, column_name, column_value):
        if column_name not in self.columns:
            # no such column
            return self.header, []
        
        col_id = self.columns[column_name]
        
        # select rows using index
        result = self.b_trees[col_id].search_key(column_value)
        if result is not None:
            x = result[0]
            i = result[1]
            selected_rows = x.key_vals[i][1]
        
        return self.header, selected_rows

    def index_exists(self, column_name):
        if column_name not in self.columns:
            # no such column
            return False
        
        col_id = self.columns[column_name]
        
        if self.b_trees[col_id] is None:
            return False
        else:
            return True
    
    def create_index(self, column_name):

        col_id = self.columns[column_name]
        self.b_trees[col_id] = BTree()
            
        for row in self.rows:
            self.b_trees[col_id].insert_key(row[col_id], row)
        
    
    
    def get_index_name(self):
        list = []
        for column in self.b_trees:
            if column is not None:                
                index_name = self.header[self.b_trees.index(column)]
                list.append(index_name)
            
        return list
        
    def get_table_header(self):
        list = []
        for column in self.header:
            list.append(column)
        return list
    
    def drop_index(self, column_name):

        col_id = self.columns[column_name]
        
        # drop the index
        self.b_trees[col_id] = None