import requests, json, time, sched, sys, argparse
from sys import argv
from flata import Flata, Query, where
from Modules import cisco
from Modules import flataDb
from Modules import driftlagetApi


#Handle command line arguments
def arguments():
    #Handle command line arguments
    parser = argparse.ArgumentParser(description='Calls the API for https://internwww.svenskakyrkan.se/Kanslist%C3%B6d/aktuellt-driftlage. And post the result in a Webex Space.')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-b', '--bottoken', help='Access token for your bot.', required=True)
    requiredNamed.add_argument('-r', '--roomid', help='The room ID.', required=True)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    return args

#build log message
def log(msg):
    timestamp = time.ctime()
    loggmsg = {'Timestamp': str(timestamp), 'Message': msg}
    return loggmsg


#Main
def main(sc):

    args = arguments()

    #Var declaration
    DriftlagetUrl = "https://webapp.svenskakyrkan.se/driftlaget/v2/api/news"
    botToken = args.bottoken
    dbPath = "mydb.json"
    dbTableName = "driftlaget"
    logdbTableName = "log"
    roomId = args.roomid

    #Get data from driftlaget.
    result = driftlagetApi.apiCallPublished(DriftlagetUrl)
    finalResult = cisco.buildJson(result)

    #Start and initialize database
    db = flataDb.initDb(dbPath, dbTableName)
    logdb = flataDb.initDb(dbPath, logdbTableName)
    q = Query()

    #Log to database
    logdb.insert(log("Starting script"))

    #Post into Webex space and update database.
    for n in finalResult:
        incidentIddb = n["IncidentId"]
        lastUpdateddb = n["LastUpdated"]
        entryExist = db.search((q.IncidentId == incidentIddb))

        #If entry is missing in the database. Insert into database and send to Webex.
        if not entryExist:
            db.insert(n)
            cisco.send_it(botToken, roomId, n)

            logdb.insert(log("New insert"))
        else:
            newEntries = db.search((q.IncidentId == incidentIddb) & (q.LastUpdated < lastUpdateddb))

            #Update new entries that have newer lastUpdated and send to Webex.
            if newEntries:
                db.update(n, where('IncidentId') == incidentIddb)
                cisco.send_it(botToken, roomId, n)

                logdb.insert(log("New update"))

    #Remove objects from database that doesnt exist on the Driftlage.
    for i in db.all():
        IncId = (i["IncidentId"])
        entryInDb = filter(lambda x : x['IncidentId'] == IncId, finalResult)
        entryInDb = list(entryInDb)

        if not entryInDb:
            db.remove(q.IncidentId == IncId)
            logdb.insert(log("New remove"))
    
    #Purge logdata if over 100 entries.
    flataDb.cleanLogDb(logdb, 100)

    #Restart the script.
    logdb.insert(log("Restarting script"))
    s.enter(30, 1, main, (sc,))

if __name__ == '__main__':
    # sched is used to schedule main function every 30 seconds.
    # for that once  main function executes in end,
    # we again schedule it to run in 30 seconds
    s = sched.scheduler(time.time, time.sleep)
    s.enter(30, 1, main, (s,))
    s.run()