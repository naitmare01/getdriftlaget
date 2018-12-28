import json
from flata import Flata, Query
from flata.storages import JSONStorage
from . import log

def init_db(db_path, table_name):
    #Create db
    db_init = Flata(db_path, storage=JSONStorage)
    #Create first table
    db_init.table(table_name, id_field='id')

    database = db_init.get(table_name)

    return database

def clean_log_db(logdb, number_of_logs):
    logdata = json.dumps(logdb.all(), indent=2)
    logdatadict = json.loads(logdata)
    log_data_count = count_log(logdatadict, number_of_logs)
    if log_data_count:
        logdb.purge()

#Counts how many data entries.
def count_log(data, number_of_logs):
    if len(data) > number_of_logs:
        return True
    else:
        return False

#Remove stale records from db that doesnt exist on the Driftlage.
def remove_stale_records(objectset, database, logdb):
    sql_query = Query()
    for i in database.all():
        inc_id = i["IncidentId"]
        #entry_in_db = filter(lambda x: x['IncidentId'] == inc_id, objectset)
        entry_in_db = [i for i in objectset if i['IncidentId'] == inc_id]
        entry_in_db = list(entry_in_db)

        if not entry_in_db:
            database.remove(sql_query.IncidentId == inc_id)

            logdb.insert(log.log("New remove on object with incidentID of: " + inc_id))
