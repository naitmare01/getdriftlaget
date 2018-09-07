# getDriftlaget
Docker container that polls the API for goo.gl/XXKFxQ. Result is posted in a Webex Temas Space from a Webex Teams Bot.

**The container must be run with two arguments.**
</br>
E.g. "docker run get-driftlaget --bottoken 'secret bot access token' --roomid 'secret room id'"

> Prerequisites
> - A Webex Teams account
> - A Webex Teams Bot
> - A Webex Teams Room

More info about Webex Teams: https://developer.webex.com/

How to
1. docker pull davidberndtsson/get-driftlaget
2. "docker run get-driftlaget --bottoken <secret bot access token> --roomid <secret room id>"
  

