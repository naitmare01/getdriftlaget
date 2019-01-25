import requests

#Get data from Driftlaget.
def get_published_messages(url):
    querystring = {"state":"published", "limit":"20", "order":"asc"}

    try:
        response = requests.request("GET", url, params=querystring, timeout=10)
        response = response.json()
        return response
    except requests.exceptions.RequestException:
        return False
