import argparse, json,sys
from flata import Flata, Query, where
from flata.storages import JSONStorage

def arguments():
    #Handle command line arguments
    parser = argparse.ArgumentParser(description='Function to list the data in the database. Choose one of the arguments.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--all', action='store_true', help='List all tables in databse.')
    group.add_argument('-l', '--log', action='store_true', help='List the table named "Log".')
    group.add_argument('-d', '--driftlaget', action='store_true', help='List the table named "driftlaget".')
    
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)
    
    return args

def initDb(dbPath, tableName):
    #Create db
    db_init = Flata(dbPath, storage=JSONStorage)
    #Create first table
    db_init.table(tableName, id_field = 'id')

    db = db_init.get(tableName)

    return db

def main():
    args = arguments()

    #Variables
    dbPath = "mydb.json"

    if args.all:
        tables = 'driftlaget', 'log'
        for i in tables:
            db = initDb(dbPath, i)
            response = db.all()
            print(json.dumps(response, indent=2))
    
    if args.log:
        tables = 'log'
        db = initDb(dbPath, tables)
        response = db.all()
        print(json.dumps(response, indent=2))

    if args.driftlaget:
        tables = 'driftlaget'
        db = initDb(dbPath, tables)
        response = db.all()
        print(json.dumps(response, indent=2))


if __name__ == '__main__':
  main()