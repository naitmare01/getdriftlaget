import requests, json

#Get data from Driftlaget. 
def getPublishedMessages(url):
    url = url
    querystring = {"state":"published","limit":"20","order":"asc"}
    
    headers = {
    'Cache-Control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    jsonresponse = json.loads(response.text)
    return jsonresponse