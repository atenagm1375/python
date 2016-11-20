import sys
import csv
import os
import shutil

def create_database(name):
    try:
        database = open(name+'.csv', 'w', newline='')
    except IOError:
        database.close()

def use_database(name):
    global table
<<<<<<< Updated upstream
    with open(name+'.csv', 'a', newline='') as database:
        table = csv.reader(database)
        while True:
            line = sys.stdin.readline()
            if line:
                t = command(line.split(' '))
                if t == 1:
                    database.close()
                    database = open(name+'.csv', 'r', newline='')
                    table = csv.reader(database)
                    for row in table:
                        if row == [line.split(' ')[2].split(';\n')[0]]:
                            t = 0
                    database.close()
                    with open(name+'.csv', 'a', newline='') as database:
                        if t == 1:
                            table = csv.writer(database)
                            table.writerow([table_name])
                            table.writerow(col_name)
                if t == 2:
                    database.close()
                    database = open(name+'.csv', 'r', newline='')
                    table = csv.reader(database)
                    for row in table:
                        if row == [line.split(' ')[2].split(';\n')[0]]:
                            for i in table.__next__():
                                print(i)
                if t == 3:
                    database.close()
                    with open(name+'.csv', 'r+', newline='') as database:
                        table = csv.reader(database)
                        line = line.split(' ')
                        for row in table:
                            if row == [line[2]]:
                                database.seek(len(row))
                        table = csv.writer(database)
                        com = line[4:]
                        print(com)
                        #com[-1] = com[-1].split(';\n')[0]
                        com = [col.split(',')[0] for col in com]
                        table.writerow(com);
            else:
                sys.exit(0)

=======
    database = open(name+'.csv', 'a')
    table = csv.reader(database)
    while True:
        line = sys.stdin.readline()
        if line:
            t = command(line.strip(';\n').split(' '))
            if t == 1:
                database.close()
                database = open(name+'.csv', 'r')
                table = csv.reader(database)
                for row in table:
                    if row == [line.strip(';\n').split(' ')[2]]:
                        t = 0
                database.close()
                database = open(name+'.csv', 'a')
                if t == 1:
                    table = csv.writer(database)
                    table.writerow([table_name])
                    table.writerow(col_name)
            if t == 2:
                database.close()
                database = open(name+'.csv', 'r')
                table = csv.reader(database)
                for row in table:
                    if row == [line.strip(';\n').split(' ')[2]]:
                        for i in table.__next__():
                            print(i)
            if t == 3:
                database.close()
                database = open(name+'.csv', 'r')
                f = open(name+'.csv.temp', 'w')
                tableR = csv.reader(database)
                tableW = csv.writer(f)
                for row in tableR:
                    print(row)
                    tableW.writerow(row)
                    if row == [line.strip(';\n').split(' ')[2]]:
                        tableW.writerow(tableR.__next__())
                        tableW.writerow(line.strip(';\n').replace(', ', ' ').split(' ')[4:])
                f.close()
                database.close()
                shutil.move(name+'.csv.temp', name+'.csv')
        else:
            sys.exit(0)
    database.close()
>>>>>>> Stashed changes

def create_table(com):
    global table_name
    table_name = com[0]
    global col_name
    com[-1] = com[-1].split(';\n')[0]
    com = [col.split(',')[0] for col in com] 
    col_name = com[2:]

def command(line):
    if line[0] == "CREATE" and line[1] == "DATABASE":
        create_database(line[2].split(';\n')[0])
        return 0
    elif line[0] == "USE" and line[1] == "DATABASE":
        use_database(line[2].split(';\n')[0])
        return 0
    elif line[0] == "CREATE" and line[1] == "TABLE":
        create_table(line[2:])
        return 1
    elif line[0] == "SHOW" and line[1] == "TABLE":
        return 2
    elif line[0] == "INSERT" and line[1] == "INTO":
        return 3

while True:
    global database
    line = sys.stdin.readline()
    if line:
       command(line.split(' '))
    else:
        sys.exit(0)
