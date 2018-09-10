# getDriftlaget
Docker container that polls the API for the Church of Sweden current IT operation status(goo.gl/XXKFxQ). Result is then posted in a Webex Temas Space from a Webex Teams Bot. Only new result will get posted, the API will be polled every 30 seconds. 

![alt text](https://github.com/naitmare01/getDriftlaget/blob/master/Private/Screen%20Shot%202018-09-07%20at%2022.18.45.png)

**The container must be run with two arguments.**

E.g. _"docker run getdriftlaget --bottoken 'secret bot access token' --roomid 'secret room id'"_


--- 
> ### Prerequisites
> - A Webex Teams account
> - A Webex Teams Bot
> - A Webex Teams Space
> - Add your bot to the space that should get notifications

More info about Webex Teams: https://developer.webex.com/

---


### **How to, pull from docker hub(recomended).**
```
1. docker pull davidberndtsson/getdriftlaget
2. docker run davidberndtsson/getdriftlaget --bottoken <secret bot access token> --roomid <secret room id>
```


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

### **Optional parameters when running image.**
```
--pollinginterval
The polling intervall in seconds. If left untouched default is 30.
I.e. how often the bot should poll the API.
```
```
--url
API URL to for the Church of Sweden current IT operation status(goo.gl/XXKFxQ). If left untouched default is https://webapp.svenskakyrkan.se/driftlaget/v2/api/news

```
```
--logthreshold
Number of entries to be keep in the log database before the databse is purged. If left untouched default is 100 logs.
```

### Contributors
https://github.com/nimok for reviewing and modified the code to the better.
