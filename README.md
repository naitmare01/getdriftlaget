# getdriftlaget

getdriftlaget is a Docker container that polls the API for the Church of Sweden current IT operation status [Driftlaget](https://internwww.svenskakyrkan.se/Kanslist%C3%B6d/aktuellt-driftlage). Result is then posted in a Webex Temas Space from a Webex Teams Bot. Only new result will get posted, by default the API will be polled every 30 seconds. 

## Getting Started

This Docker container can be run localy or in any of the cloud providers that has Docker and/or Kubernetes. 

### Prerequisites

- A Webex Teams account
- A Webex Teams Bot, including the access token
- A Webex Teams Space, including the room id
- The bot needs to added to the space that should get notifications

```
More info about Webex Teams and the API: [Webex Developer](https://developer.webex.com/)
```

### Installing

A step by step series of examples that describes how to install the container on Docker. 

How to, pull from docker hub(recomended). 
This instruction will run the bot every 30 seconds and post new updates to the Webex Teams Space specified in the parameter "roomid"

```
1. docker pull davidberndtsson/getdriftlaget:latest
2. docker run davidberndtsson/getdriftlaget:latest --bottoken <secret bot access token> --roomid <secret room id>
```

How to, download code and build image
This instruction will clone the project to your local machine and start the bot. 
The bot will run every 30 second and post new updates to the Webex Teams Space specified in the parameter "roomid"

```
1. [Install docker](https://docs.docker.com/v17.12/install/)
2. [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
3. Open bash, terminal or powershell
4. mkdir gitprojects
5. cd gitprojects
6. git clone https://github.com/naitmare01/getdriftlaget
7. docker build -t get-driftlaget:latest .
8. docker run get-driftlaget:latest --bottoken <secret bot access token> --roomid <secret room id>
```

## Mandatory parameters when running image
```
--bottoken
Access token for your bot. See [Webex Developer](https://developer.webex.com/)
```
```
--roomid
The room ID of the Webex Space. See [Webex Developer](https://developer.webex.com/)

```

## Optional parameters when running image
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
```
--database
Full path to database file. Make sure to include file.json after the full path. If left untouched default is mydb.json.
E.g. --database /usr/share/db/mydb.json

```

<img src="https://raw.githubusercontent.com/naitmare01/getDriftlaget/master/Private/Screen%20Shot%202018-09-07%20at%2022.18.45.png" class="img-responsive" alt="">

## Built With

* [Python3](https://www.python.org/) - The coding language
* [Flata](https://github.com/harryho/flata) - The database enginge

## Contributing

Open a new issue with the label [contributin](https://github.com/naitmare01/getdriftlaget/labels/contributing) and we'll get in touch!

## Versioning

For the versions available, see the [tags on this repository](https://github.com/naitmare01/getdriftlaget/tags). 

## Authors

* **David Berndtsson** - *Initial work* - [naitmare01](https://github.com/naitmare01)
* **Erik Ohlsson** - *Reviewing and modified the code to the better.* - [nimok](https://github.com/nimok) 

See also the list of [contributors](https://github.com/naitmare01/getdriftlaget/graphs/contributors) who participated in this project.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
