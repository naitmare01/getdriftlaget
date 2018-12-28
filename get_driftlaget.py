import sched
import argparse
import time
from services import webex_teams, flata_db, driftlaget_api, log

#Handle command line arguments
def arguments():

    parser = argparse.ArgumentParser(description='Calls the API for https://internwww.svenskakyrkan.se/Kanslist%C3%B6d/aktuellt-driftlage. And post the result in a Webex Space.')

    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-b', '--bottoken', help='Access token for your bot.', required=True)
    required_named.add_argument('-r', '--roomid', help='The room ID.', required=True)
    parser.add_argument('-p', '--pollinginterval', help='The polling intervall in seconds. If left untouched default is 30.', type=int, default=30)
    parser.add_argument('-u', '--url', help='API URL to for the Church of Sweden current IT operation status(goo.gl/XXKFxQ). If left untouched default is https://webapp.svenskakyrkan.se/driftlaget/v2/api/news', default='https://webapp.svenskakyrkan.se/driftlaget/v2/api/news')
    parser.add_argument('-lt', '--logthreshold', help='Number of entries to be keep in the log database before the databse is purged. If left untouched default is 100', type=int, default=100)
    parser.add_argument('-db', '--database', help='Full path to database file. Make sure to include file.json after the full path. If left untouched default is mydb.json', default='mydb.json')

    return parser.parse_args()

#Main
def main(script_scheduler):
    args = arguments()

    #Var declaration
    driftlageturl = args.url
    bot_token = args.bottoken
    room_id = args.roomid
    polling_interval = args.pollinginterval
    logthreshold = args.logthreshold
    db_path = args.database
    db_table_name = "driftlaget"
    logdb_table_name = "log"

    #Get data from driftlaget.
    published_messages = driftlaget_api.get_published_messages(driftlageturl)
    json_for_webex_teams = webex_teams.build_json(published_messages)

    #Start and initialize database with two tables
    database_file = flata_db.init_db(db_path, db_table_name)
    logdb = flata_db.init_db(db_path, logdb_table_name)

    #Log to database
    logdb.insert(log.log("Starting script"))

    #Post into Webex space and update database.
    webex_teams.post_to_space(json_for_webex_teams, database_file, logdb, bot_token, room_id)

    #Remove objects from database that doesnt exist on the Driftlage and log action to database.
    flata_db.remove_stale_records(json_for_webex_teams, database_file, logdb)

    #Purge logdata if over 100 entries.
    flata_db.clean_log_db(logdb, logthreshold)

    #Restart the script.
    logdb.insert(log.log("Restarting script"))
    S.enter(polling_interval, 1, main, (script_scheduler,))

if __name__ == '__main__':
    # sched is used to schedule main function every 30 seconds.
    # for that once  main function executes in end,
    # we again schedule it to run in 30 seconds
    S = sched.scheduler(time.time, time.sleep)
    S.enter(arguments().pollinginterval, 1, main, (S,))
    S.run()
