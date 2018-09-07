import requests, json, time, sched, sys, argparse
from datetime import datetime
from flata import Flata, Query, where
from flata.storages import JSONStorage
from sys import argv


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

#Get data from Dirftlaget. 
def apiCall(url):
    url = url
    querystring = {"state":"published","limit":"20","order":"asc"}
    
    headers = {
    'Cache-Control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    jsonresponse = json.loads(response.text)
    return jsonresponse

#Send data to Cisco Teams space. 
def send_it(token, room_id, message):
    header = {"Authorization": "Bearer %s" % token,
                "Content-Type": "application/json"}

    data = {"roomId": room_id,
            "markdown": ">* **" + message["Subject"] + "** " 
            + " \n " + message["Type"] 
            + "  \n" + " Starttid: " + message["StartDate"] 
            + "  \n" + " Sluttid: " + message["EndDate"] 
            + "  \n" + "Senast uppdaterad: " + message["LastUpdated"] 
            + "  \n" + "Kategori: " + message["Categories"]
            + "  \n" + "IncidentID: " + message["IncidentId"]
            }
    return requests.post("https://api.ciscospark.com/v1/messages/", headers=header, data=json.dumps(data), verify=True)

#Format time
def formatTime(time): 
    sep = "."
    formatedTime = time.split(sep, 1)[0]
    formatedTime = formatedTime.replace('T', '')
    formatedTime = datetime.strptime(formatedTime, "%Y%m%d%H%M%S")

    return formatedTime

#Build custom json result of api-call
def buildJson(jsonObject):

    result = []

    for n in jsonObject["Results"]:
        subject = n["Subject"]
        startdate = n["StartDate"]
        enddate = n["EndDate"]
        lastUpdated = n["Updated"]
        tags = ""
        incidentId = n["Id"]

        if n["NewsType"]:
            type = type = n["NewsType"]["Name"]
        else: 
            type = "N/A"

        for c in n["Categories"]:
            Categories = c["Name"]
            tags = tags + ", " + Categories

        tags = tags[2:]

        startdate = formatTime(startdate)
        startdate = str(startdate)

        enddate = formatTime(enddate)
        enddate = str(enddate)

        lastUpdated = formatTime(lastUpdated)
        lastUpdated = str(lastUpdated)

        data = {'Subject': subject, 'Type': type, 'StartDate': startdate, 'EndDate': enddate, 'Categories': tags, 'LastUpdated': lastUpdated, 'IncidentId': incidentId}
        result.append(data.copy())

    return result

#Init DB
def initDb(dbPath, tableName):
    #Create db
    db_init = Flata(dbPath, storage=JSONStorage)
    #Create first table
    db_init.table(tableName, id_field = 'id')

    db = db_init.get(tableName)

    return db

#build log message
def log(msg):
    timestamp = time.ctime()
    loggmsg = {'Timestamp': str(timestamp), 'Message': msg}
    return loggmsg

#Counts how many log entries. 
def countLog(data):
    if len(data) > 100:
        return True
    else:
        return False

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
    result = apiCall(DriftlagetUrl)
    finalResult = buildJson(result)

    #Start and initialize database
    db = initDb(dbPath, dbTableName)
    logdb = initDb(dbPath, logdbTableName)
    q = Query()

    logmessage = log("Starting script")
    logdb.insert(logmessage)

    #Post into Webex space and update database.
    for n in finalResult:
        incidentIddb = n["IncidentId"]
        lastUpdateddb = n["LastUpdated"]
        entryExist = db.search((q.IncidentId == incidentIddb))

        #If entry is missing in the database. Insert into database and send to Webex.
        if not entryExist:
            db.insert(n)
            send_it(botToken, roomId, n)

            logmessage = log("New insert")
            logdb.insert(logmessage)
        else:
            newEntries = db.search((q.IncidentId == incidentIddb) & (q.LastUpdated < lastUpdateddb))

            #Update new entries that have newer lastUpdated and send to Webex.
            if newEntries:
                db.update(n, where('IncidentId') == incidentIddb)
                send_it(botToken, roomId, n)

                logmessage = log("New update")
                logdb.insert(logmessage)

    #Remove objects from database that doesnt exist on the Driftlage.
    for i in db.all():
        IncId = (i["IncidentId"])
        entryInDb = filter(lambda x : x['IncidentId'] == IncId, finalResult)
        entryInDb = list(entryInDb)

        if not entryInDb:
            #print(IncId + " exist in database but not on website.")
            db.remove(q.IncidentId == IncId)
            logmessage = log("New remove")
            logdb.insert(logmessage)
    
    #Restart the script. Purge logdata if over 100 entries.
    logmessage = log("Restarting script")
    logdb.insert(logmessage)
    logdata = json.dumps(logdb.all(), indent=2)
    logdatadict = json.loads(logdata)
    logDataCount = countLog(logdatadict)
    if logDataCount == True:
        logdb.purge()
    s.enter(30, 1, main, (sc,))

if __name__ == '__main__':
    # sched is used to schedule main function every 30 seconds.
    # for that once  main function executes in end,
    # we again schedule it to run in 30 seconds
    s = sched.scheduler(time.time, time.sleep)
    s.enter(30, 1, main, (s,))
    s.run()