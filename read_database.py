import argparse
import json
import sys
from services import flataDb

def arguments():
    #Handle command line arguments
    parser = argparse.ArgumentParser(description='Function to list the data in the database. Choose one of the arguments.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--all', action='store_true', help='List all tables in databse.')
    group.add_argument('-l', '--log', action='store_true', help='List the table named "Log".')
    group.add_argument('-d', '--driftlaget', action='store_true', help='List the table named "driftlaget".')
    parser.add_argument('-db', '--database', help='Full path to database file. Make sure to include file.json after the full path. If left untouched default is mydb.json', default='mydb.json')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    return args

def main():
    args = arguments()

    #Variables
    db_path = args.database

    if args.all:
        tables = 'driftlaget', 'log'
        for i in tables:
            database_file = flataDb.initDb(db_path, i)
            response = database_file.all()
            print("Reading data from table:", i, '\n', json.dumps(response, indent=2))

    if args.log:
        tables = 'log'
        database_file = flataDb.initDb(db_path, tables)
        response = database_file.all()
        print("Reading data from table:", tables, '\n', json.dumps(response, indent=2))

    if args.driftlaget:
        tables = 'driftlaget'
        database_file = flataDb.initDb(db_path, tables)
        response = database_file.all()
        print("Reading data from table:", tables, '\n', json.dumps(response, indent=2))


if __name__ == '__main__':
    main()
