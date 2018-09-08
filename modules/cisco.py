import requests, json
from datetime import datetime


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
