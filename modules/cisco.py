import requests, json
from datetime import datetime
from flata import Query, where
from . import log


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

#Build custom json result of api-call before sending to Cisco Teams space.
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

#Format time
def formatTime(time): 
    sep = "."
    formatedTime = time.split(sep, 1)[0]
    formatedTime = formatedTime.replace('T', '')
    formatedTime = datetime.strptime(formatedTime, "%Y%m%d%H%M%S")

    return formatedTime


#Post into Webex space and update database.
def postToSpace(objectset, database, logdb, botToken, roomId):
    q = Query()
    for n in objectset:
        incidentIddb = n["IncidentId"]
        lastUpdateddb = n["LastUpdated"]
        entryExist = database.search((q.IncidentId == incidentIddb))

        #If entry is missing in the database. Insert into database and send to Webex.
        if not entryExist:
            database.insert(n)
            send_it(botToken, roomId, n)

            logdb.insert(log.log("New insert on object with incidentID of: " + incidentIddb))
        else:
            newEntries = database.search((q.IncidentId == incidentIddb) & (q.LastUpdated < lastUpdateddb))

            #Update new entries that have newer lastUpdated and send to Webex.
            if newEntries:
                database.update(n, where('IncidentId') == incidentIddb)
                send_it(botToken, roomId, n)

                logdb.insert(log.log("New update on object with incidentID of: " + incidentIddb))