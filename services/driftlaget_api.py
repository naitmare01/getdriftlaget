import json
import requests

#Get data from Driftlaget.
def get_published_messages(url):
    url = url
    querystring = {"state":"published", "limit":"20", "order":"asc"}

    headers = {
        'Cache-Control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    jsonresponse = json.loads(response.text)
    return jsonresponse
