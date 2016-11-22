import sys
import csv
import os
import shutil

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
    database_name = line[2]+'.csv'
    try:
        database = open(database_name, 'a')
        database.close()
    except IOError:
        print('>>NO FILE NAMED '+database_name)

def show_table(line):
    if not line[1].lower() == 'table':
        syntax_error(line)
        return
    database = open(database_name, 'r')
    table = csv.reader(database)
    found = False
    for row in table:
        if row == [line[2]]:
            found = True
            for i in next(table):
                print(i)
    if not found:
        print('>>NO SUCH TABLE!')
    database.close()

def create_table(line):
    if not line[3].lower() == 'columns':
        syntax_error(line)
        return
    database = open(database_name, 'r')
    table = csv.reader(database)
    found = False
    for row in table:
        if row == [line[2]]:
            found = True
            print('>>TABLE ALREADY EXISTS')
    database.close()
    if not found:
        database = open(database_name, 'a')
        table = csv.writer(database)
        table.writerow([line[2]])
        table.writerow(line[4:])

def insert_into(line):
    if not line[3].lower() == 'values' or not line[1].lower() == 'into':
        syntax_error(line)
        return
    database = open(database_name, 'r')
    temp = open(database_name+'.temp', 'w')
    tableR = csv.reader(database)
    tableW = csv.writer(temp)
    found = False
    for row in tableR:
        tableW.writerow(row)
        if row == [line[2]]:
            found = True
            tableW.writerow(next(tableR))
            tableW.writerow(line[4:])
    temp.close()
    database.close()
    shutil.move(database_name+'.temp', database_name)
    if not found:
        print('>>NO SUCH TABLE!')

def select(line):
    if not line[2].lower() == 'from':
        syntax_error(line)
        return
    database = open(database_name, 'r')
    table = csv.reader(database)
    query = []
    found = False
    temp = False
    for row in table:
        if row == [line[3]]:
            found = True
            row = next(table)
            i = 0
            while temp and i < len(row):
                if row[i] == line[1]:
                    r = next(table)
                    while len(row) == len(r):
                        query.append(r[i])
                        try:
                            r = next(table)
                        except StopIteration:
                            temp = True
                            break
                        temp = True
                i += 1
        if temp:
            break
    database.close()
    if not temp:
        print('>>NO SUCH QUERY!')
        return
    for i in range(len(query)):
        print(query[-(i + 1)])

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

global database_name
while True:
    line = sys.stdin.readline()
    if line:
        command(line.strip(';\n').replace(', ', ' ').split(' '))
    else:
        sys.exit(0)
