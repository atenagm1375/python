import sys
import csv

def create_database(name):
    try:
        database = open(name+'.csv', 'w', newline='')
    except IOError:
        database.close()

def use_database(name):
    global table
    with open(name+'.csv', 'r+', newline='') as database:
        table = csv.reader(database)
        while True:
            line = sys.stdin.readline()
            if line:
                t = command(line.split(' '))
                if t:
                    table = csv.writer(database)
                    table.writerow([table_name])
                    table.writerow(col_name)

            else:
                sys.exit(0)


def create_table(com):
    global table_name
    table_name = com[0]
    global col_name
    com[-1] = com[-1].split(';\n')[0]
    com = [col.split(',')[0] for col in com] 
    col_name = com[2:]

def show_table(name):
    if name == table_name:
        for col in col_name:
            print(col)
    

def command(line):
    if line[0] == "CREATE" and line[1] == "DATABASE":
        create_database(line[2].split(';\n')[0])
        return False
    elif line[0] == "USE" and line[1] == "DATABASE":
        use_database(line[2].split(';\n')[0])
        return False
    elif line[0] == "CREATE" and line[1] == "TABLE":
        create_table(line[2:])
        return True
    elif line[0] == "SHOW" and line[1] == "TABLE":
        show_table(line[2].split(';\n')[0])
        return False

while True:
    global database
    line = sys.stdin.readline()
    if line:
       command(line.split(' '))
    else:
        sys.exit(0)
