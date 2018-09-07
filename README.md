# getDriftlaget
Docker container that polls the API for the Church of Sweden current IT operation status(goo.gl/XXKFxQ). Result is then posted in a Webex Temas Space from a Webex Teams Bot.

**The container must be run with two arguments.**
</br>
E.g. _"docker run get-driftlaget --bottoken 'secret bot access token' --roomid 'secret room id'"_
</br>

--- 
> ### Prerequisites
> - A Webex Teams account
> - A Webex Teams Bot
> - A Webex Teams Room
</br>
More info about Webex Teams: https://developer.webex.com/

---

### **How to**
```
1. docker pull davidberndtsson/get-driftlaget
2. "docker run davidberndtsson/get-driftlaget --bottoken <secret bot access token> --roomid <secret room id>"
```
  

