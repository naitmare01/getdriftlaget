from flata import Flata, Query, where
from flata.storages import JSONStorage
import json

def initDb(dbPath, tableName):
    #Create db
    db_init = Flata(dbPath, storage=JSONStorage)
    #Create first table
    db_init.table(tableName, id_field = 'id')

    db = db_init.get(tableName)

    return db

def cleanLogDb(logdb, numberOfLogs):
    logdata = json.dumps(logdb.all(), indent=2)
    logdatadict = json.loads(logdata)
    logDataCount = countLog(logdatadict, numberOfLogs)
    if logDataCount == True:
        logdb.purge()

#Counts how many data entries. 
def countLog(data, numberOfLogs):
    if len(data) > numberOfLogs:
        return True
    else:
        return False

