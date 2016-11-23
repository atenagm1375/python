import sys
import csv
import shutil

def create(line):
    com = {'database': create_database, 'table': create_table, 'error': syntax_error}
    if line[1].lower() in com:
        com[line[1].lower()](line)
    else:
        com['error']()

def create_database(line):
    if len(line) != 3:
        syntax_error()
        return
    try:
        if line[2] == '':
            syntax_error()
            return
        database = open(line[2]+'.csv', 'w')
        database.close()
    except IOError:
        print('...>>ERROR WHILE CREATING FILE\nTRY AGAIN...')

def use_database(line):
    if len(line) != 3:
        syntax_error()
        return
    if not line[1].lower() == 'database':
        syntax_error()
        return
    global database_name
    if line[2] == '':
        syntax_error()
        return
    database_name = line[2]+'.csv'
    try:
        database = open(database_name, 'r')
        database.close()
    except IOError:
        print('...>>NO FILE NAMED '+database_name)

def show_table(line):
    if len(line) != 3:
        syntax_error()
        return
    if not line[1].lower() == 'table':
        syntax_error()
        return
    try:
        database = open(database_name, 'r')
    except NameError:
        print('...>>CHOOSE THE DATABASE USING "USE DATABASE" COMMAND FIRST')
        return
    table = csv.reader(database)
    found = False
    for row in table:
        if [line[2]] == row:
            found = True
            for i in next(table):
                print(i)
    if not found:
        print('...>>NO SUCH TABLE!')
    database.close()

def create_table(line):
    if not line[3].lower() == 'columns':
        syntax_error()
        return
    if line[2] == '':
        syntax_error()
        return
    try:
        database = open(database_name, 'r')
    except NameError:
        print('...>>CHOOSE THE DATABASE USING \'USE DATABASE\' COMMAND FIRST')
        return
    table = csv.reader(database)
    found = False
    for row in table:
        if [line[2]] == row:
            found = True
            print('...>>TABLE ALREADY EXISTS')
    database.close()
    if not found:
        database = open(database_name, 'a')
        table = csv.writer(database)
        table.writerow([line[2]])
        table.writerow(line[4:])
        table.writerow([])
        database.close()

def insert_into(line):
    if not line[3].lower() == 'values' or not line[1].lower() == 'into':
        syntax_error()
        return
    try:
        database = open(database_name, 'r+')
    except NameError:
        print('...>>CHOOSE THE DATABASE USING \'USE DATABASE\' COMMAND FIRST')
        return
    temp = open(database_name+'.temp', 'w')
    tableR = csv.reader(database)
    tableW = csv.writer(temp)
    found = False
    for row in tableR:
        tableW.writerow(row)
        if [line[2]] == row:
            a = next(tableR)
            if len(a) != len(line[4:]):
                print('...>>COLUMNS AND VALUES MISMATCH IN NUMBER')
                return
            found = True
            tableW.writerow(a)
            tableW.writerow(line[4:])
    temp.close()
    database.close()
    shutil.move(database_name+'.temp', database_name)
    if not found:
        print('...>>NO SUCH TABLE!')

def select(line):
    if len(line) != 4:
        syntax_error()
        return
    if not line[2].lower() == 'from':
        syntax_error()
        return
    try:
        database = open(database_name, 'r')
    except NameError:
        print('...>>CHOOSE THE DATABASE USING \'USE DATABASE\' COMMAND FIRST')
        return
    table = csv.reader(database)
    query = []
    found_table = False
    found_query = False
    for row in table:
        if [line[3]] == row:
            found_table = True
            row = next(table)
            i = 0
            while not found_query and i < len(row):
                if row[i] == line[1]:
                    found_query = True
                    r = next(table)
                    while r != []:
                        query.append(r[i])
                        try:
                            r = next(table)
                        except StopIteration:
                            break
                i += 1
        if found_query:
            break
    database.close()
    if not found_query:
        print('...>>NO SUCH QUERY!')
        return
    if not found_table:
        print('...>>NO SUCH TABLE!')
        return
    for i in range(len(query)):
        print(query[-(i + 1)])

def syntax_error():
    print('...>>INVALID SYNTAX<<')

def command(line):
    com = {'create': create,
            'use': use_database,
            'show': show_table,
            'insert': insert_into,
            'select': select,
            'error': syntax_error}
    if line[0].lower() in com:
        com[line[0].lower()](line)
    else:
        com['error']()

while True:
    try:
        line = input('>>> ')
        command(line.strip(';\n').replace(', ', ' ').split(' '))
    except EOFError:
        sys.exit(0)
