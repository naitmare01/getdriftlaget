import json
from datetime import datetime
import requests
from flata import Query, where
from . import log

#Remove whitespace from trailing and leading
def remove_whitespace(text):
    cleanedtext = text.rstrip().lstrip()

    return cleanedtext

#Send data to Cisco Teams space.
def send_it(token, room_id, message):
    header = {"Authorization": "Bearer %s" % token, "Content-Type": "application/json"}

    data = {"roomId": room_id, "markdown": ">* **" + message["Subject"] + "** " + " \n " + message["Type"] + "  \n" + " Starttid: " + message["StartDate"] + "  \n" + " Sluttid: " + message["EndDate"] + "  \n" + "Senast uppdaterad: " + message["LastUpdated"] + "  \n" + "Kategori: " + message["Categories"] + "  \n" + "IncidentID: " + message["IncidentId"]}
    return requests.post("https://api.ciscospark.com/v1/messages/", headers=header, data=json.dumps(data), verify=True, timeout=10)

#Remove post from Cisco Webex teams.
def remove_it(token, message_id):
    url = "https://api.ciscospark.com/v1/messages/" + message_id

    headers = {"Authorization": "Bearer %s" % token}

    response = requests.request("DELETE", url, headers=headers, timeout=10)

    return response.text

#Build custom json result of api-call before sending to Cisco Teams space.
def build_json(json_object):

    result = []

    for item in json_object["Results"]:
        subject = item["Subject"]
        startdate = item["StartDate"]
        enddate = item["EndDate"]
        last_updated = item["Updated"]
        tags = ""
        incident_id = item["Id"]

        #Clean whitespace from subject to avoid formating error when posting to space.
        subject = remove_whitespace(subject)

        if item["NewsType"]:
            incident_type = item["NewsType"]["Name"]
        else:
            incident_type = "N/A"

        for sub_categories in item["Categories"]:
            categories = sub_categories["Name"]
            tags = tags + ", " + categories

        tags = tags[2:]

        startdate = format_time(startdate)
        startdate = str(startdate)

        enddate = format_time(enddate)
        enddate = str(enddate)

        last_updated = format_time(last_updated)
        last_updated = str(last_updated)

        data = {'Subject': subject, 'Type': incident_type, 'StartDate': startdate, 'EndDate': enddate, 'Categories': tags, 'LastUpdated': last_updated, 'IncidentId': incident_id}
        result.append(data.copy())

    return result

#Format time
def format_time(time):
    sep = "."
    formated_time = time.split(sep, 1)[0]
    formated_time = formated_time.replace('T', '')
    formated_time = datetime.strptime(formated_time, "%Y%m%d%H%M%S")

    return formated_time

#Post into Cisco Webex space and update database.
def post_to_space(objectset, database, logdb, bot_token, room_id):
    sql_query = Query()
    for item in objectset:
        incident_id_db = item["IncidentId"]
        last_updated_db = item["LastUpdated"]
        entry_exist = database.search((sql_query.IncidentId == incident_id_db))

        #If entry is missing in the database. Insert into database and send to Webex.
        if not entry_exist:
            sendrespone = send_it(bot_token, room_id, item)
            msg_id = sendrespone.json()
            msg_id = msg_id["id"]
            item['msgId'] = msg_id
            database.insert(item)

            logdb.insert(log.log("New insert on object with incidentID of: " + incident_id_db))
        else:
            new_entries = database.search((sql_query.IncidentId == incident_id_db) & (sql_query.LastUpdated < last_updated_db))

            #Update new entries that have newer lastUpdated and send to Webex.
            if new_entries:
                database.update(item, where('IncidentId') == incident_id_db)
                send_it(bot_token, room_id, item)

                logdb.insert(log.log("New update on object with incidentID of: " + incident_id_db))
