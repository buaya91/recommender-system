#-------------------------------------------------------------------------------
# Name:        Pre-processing script
# Purpose:     To obtain useful data from raw data set
#
# Author:      ASUS-PC
#
# Created:     26/09/2014
# Copyright:   (c) ASUS-PC 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import csv
import copy

def filter_by_col(col_filter,dict_reader,dict_writer):
    '''
    col_filter is a function return true for col we want, else false
    dict_reader is associate to the file, read csv record into dict
    dict_writer is associate to the file, write dict into csv records
    return a file object
    '''
    rows = []
    for row in dict_reader:
        row_copy = copy.deepcopy(row)
        for each_col in row:
            if col_filter(each_col) is False:
                row_copy.pop(each_col)
        rows.append(row_copy)
    dict_writer.writeheader()
    dict_writer.writerows(rows)
    pass

def col_filter_creator(wanted_col):

    def col_fil(col):
        for uc in wanted_col:
            if col == uc:
                return True
        return False

    return col_fil

# group by col
def group_by_col(col_name,dict_reader,dict_writer):
    """
    read data from reader, and group them into format of
    """
    pass

def main():
    col_wanted_ordered = ['cus','item','sales']
    my_col_filter = col_filter_creator(col_wanted_ordered)
    d_reader = csv.DictReader(open('test.csv',newline=''),delimiter=',')
    d_writer = csv.DictWriter(open('test_output.csv','w',newline=''),col_wanted_ordered)
    filter_by_col(my_col_filter,d_reader,d_writer)
    pass

if __name__ == '__main__':
    main()
