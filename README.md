# getDriftlaget
Docker container that polls the API for the Church of Sweden current IT operation status(goo.gl/XXKFxQ). Result is then posted in a Webex Temas Space from a Webex Teams Bot. Only new result will get posted, the API will be polled every 30 seconds. 

![alt text(https://github.com/naitmare01/getDriftlaget/blob/master/Screen%20Shot%202018-09-07%20at%2022.18.45.png)

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
</br>

### **How to, pull from docker hub(recomended).**
```
1. docker pull davidberndtsson/get-driftlaget
2. docker run davidberndtsson/get-driftlaget --bottoken <secret bot access token> --roomid <secret room id>
```
</br>

### **How to, download code and build image.**
```
1. Install docker, https://docs.docker.com/v17.12/install/
2. Open terminal or powershell
3. mkdir getDriftlaget
4. cd getDriftlaget
5. git clone https://github.com/naitmare01/getDriftlaget
6. docker build -t get-driftlaget .
7. docker run get-driftlaget --bottoken 'secret bot access token' --roomid 'secret room id'
```

