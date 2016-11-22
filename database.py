import sys
import csv
import os
import shutil
import ast

def create_database(line):
    try:
        database = open(line[2]+'.csv', 'w')
        database.close()
    except IOError:
        print('>>ERROR WHILE CREATING FILE\nTRY AGAIN...')

def use_database(line):
    if not line[1].lower() == 'database':
        syntax_error(line)
        return
    global database_name
    database_name = line[2]+'.csv'
    try:
        database = open(database_name, 'r')
        database.close()
    except IOError:
        print('>>NO FILE NAMED '+database_name)

def show_table(line):
    if not line[1].lower() == 'table':
        syntax_error(line)
        return
    try:
        database = open(database_name, 'r')
    except NameError:
        print('>>CHOOSE THE DATABASE USING \'USE DATABASE\' COMMAND FIRST')
        return
    table = csv.DictReader(database)
    found = False
    for row in table:
        if line[2] in row:
            found = True
            for i in ast.literal_eval(row[line[2]]):
                print(i)
    if not found:
        print('>>NO SUCH TABLE!')
    database.close()

def create_table(line):
    if not line[3].lower() == 'columns':
        syntax_error(line)
        return
    try:
        database = open(database_name, 'r')
    except NameError:
        print('>>CHOOSE THE DATABASE USING \'USE DATABASE\' COMMAND FIRST')
        return
    table = csv.DictReader(database)
    found = False
    for row in table:
        if line[2] in row:
            found = True
            print('>>TABLE ALREADY EXISTS')
    database.close()
    if not found:
        database = open(database_name, 'w')
        table = csv.DictWriter(database, [line[2]])
        table.writeheader()
        table.writerow({line[2]: line[4:]})

def insert_into(line):
    if not line[3].lower() == 'values' or not line[1].lower() == 'into':
        syntax_error(line)
        return
    try:
        database = open(database_name, 'r+')
    except NameError:
        print('>>CHOOSE THE DATABASE USING \'USE DATABASE\' COMMAND FIRST')
        return
    tableR = csv.DictReader(database)
    found = False
    columns = []
    for row in tableR:
        if line[2] in row:
            found = True
            columns = ast.literal_eval(row[line[2]])
    tableW = csv.DictWriter(database, columns)
    tableW.writerow(dict(zip(columns, line[4:])))
    database.close()
    if not found:
        print('>>NO SUCH TABLE!')

def select(line):
    if not line[2].lower() == 'from':
        syntax_error(line)
        return
    try:
        database = open(database_name, 'r')
    except NameError:
        print('>>CHOOSE THE DATABASE USING \'USE DATABASE\' COMMAND FIRST')
        return
    table = csv.DictReader(database)
    found_table = False
    found_query = False
    for row in table:
        if line[3] in row:
            found_table = True
            l = ast.literal_eval(row[line[3]])
            tableR = csv.DictReader(database, l)
            print(row)
            for r in tableR:
                print(r)
                if line[1] in r:
                    found_query = True
                    print(r[line[1]])
    database.close()
    if not found_query:
        print('>>NO SUCH QUERY!')
        return
    if not found_table:
        print('>>NO SUCH TABLE!')
        return

def syntax_error(line):
    print('>>INVALID SYNTAX<<')

def command(line):
    if line[0].lower() == 'create' and line[1].lower() == 'database':
        create_database(line)
    elif line[0].lower() == 'use':
        use_database(line)
    elif line[0].lower() == 'show':
        show_table(line)
    elif line[0].lower() == 'create' and line[1].lower() == 'table':
        create_table(line)
    elif line[0].lower() == 'insert':
        insert_into(line)
    elif line[0].lower() == 'select':
        select(line)
    else:
        syntax_error(line)

while True:
    line = sys.stdin.readline()
    if line:
        command(line.strip(';\n').replace(', ', ' ').split(' '))
    else:
        sys.exit(0)
