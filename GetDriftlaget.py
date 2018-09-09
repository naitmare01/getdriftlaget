import requests, json, sched, sys, argparse, time
from sys import argv
from flata import Flata, where
from Modules import cisco, flataDb, driftlagetApi, log


#Handle command line arguments
def arguments():
    #Handle command line arguments
    parser = argparse.ArgumentParser(description='Calls the API for https://internwww.svenskakyrkan.se/Kanslist%C3%B6d/aktuellt-driftlage. And post the result in a Webex Space.')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-b', '--bottoken', help='Access token for your bot.', required=True)
    requiredNamed.add_argument('-r', '--roomid', help='The room ID.', required=True)
    parser.add_argument('-p', '--pollinginterval', help='The polling intervall in seconds. If left untouched default is 30.', type=int, default=30)
    parser.add_argument('-u', '--url', help='API URL to for the Church of Sweden current IT operation status(goo.gl/XXKFxQ). If left untouched default is https://webapp.svenskakyrkan.se/driftlaget/v2/api/news', default='https://webapp.svenskakyrkan.se/driftlaget/v2/api/news')
    parser.add_argument('-lt', '--logthreshold', help='Number of entries to be keep in the log database before the databse is purged. If left untouched default is 100', type=int, default=100)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    return args

#Main
def main(sc):

    #args = arguments()

    #Var declaration
    DriftlagetUrl = args.url
    botToken = args.bottoken
    roomId = args.roomid
    pollingInterval = args.pollinginterval
    logthreshold = args.logthreshold
    dbPath = "mydb.json"
    dbTableName = "driftlaget"
    logdbTableName = "log"

    #Get data from driftlaget.
    result = driftlagetApi.apiCallPublished(DriftlagetUrl)
    finalResult = cisco.buildJson(result)

    #Start and initialize database with two tables
    db = flataDb.initDb(dbPath, dbTableName)
    logdb = flataDb.initDb(dbPath, logdbTableName)

    #Log to database
    logdb.insert(log.log("Starting script"))

    #Post into Webex space and update database.
    cisco.postToSpace(finalResult, db, logdb, botToken, roomId)

    #Remove objects from database that doesnt exist on the Driftlage and log action to database.
    flataDb.removeStaleRecords(finalResult, db, logdb)

    #Purge logdata if over 100 entries.
    flataDb.cleanLogDb(logdb, logthreshold)

    #Restart the script.
    logdb.insert(log.log("Restarting script"))
    s.enter(pollingInterval, 1, main, (sc,))

if __name__ == '__main__':
    args = arguments()
    # sched is used to schedule main function every 30 seconds.
    # for that once  main function executes in end,
    # we again schedule it to run in 30 seconds
    s = sched.scheduler(time.time, time.sleep)
    s.enter(args.pollinginterval, 1, main, (s,))
    s.run()