import sys
import csv

def create_database(name):
    file = open(name[0]+'.csv', 'w', newline='')

def use_database(name):
    global databse
    with open(name[0]+'.csv', 'r+', newline='') as database:
        spamreader = csv.reader(database, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(row)

def create_table(com):
    global table_name
    table_name = com[0]
    global col_name
    com[-1] = com[-1].split(';\n')[0]
    col_name = com[2:]
    print(table_name)
    print(col_name)
    

def command(line):
    if line[0] == "CREATE" and line[1] == "DATABASE":
        create_database(line[2].split(';\n'))
    elif line[0] == "USE" and line[1] == "DATABASE":
        use_database(line[2].split(';\n'))
    elif line[0] == "CREATE" and line[1] == "TABLE":
        create_table(line[2:])

while True:
    line = sys.stdin.readline()
    if line:
       command(line.split(' '))
    else:
        sys.exit(0)
