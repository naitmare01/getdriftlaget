import json
from flata import Flata, Query, where
from flata.storages import JSONStorage
from . import log
from . import webexTeams

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

#Remove stale records from db that doesnt exist on the Driftlage.
def removeStaleRecords(objectset, database, logdb, token):
    q = Query()
    for i in database.all():
        IncId = i["IncidentId"]
        entryInDb = filter(lambda x : x['IncidentId'] == IncId, objectset)
        entryInDb = list(entryInDb)

        if not entryInDb:
            database.remove(q.IncidentId == IncId)
            
            #Remove post from Cisco Webex Teams that are no longer active
            #webexTeams.remove_it(token, i["msgId"])

            logdb.insert(log.log("New remove on object with incidentID of: " + IncId))