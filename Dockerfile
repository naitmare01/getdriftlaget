FROM ubuntu:latest
LABEL David Berndtsson
RUN apt-get update -y
RUN apt-get -qqy install python3
RUN apt-get -qqy install python3-pip
COPY . /main
WORKDIR /main
RUN pip3 install -r requirements.txt
RUN touch /main/mydb.json
ADD GetDriftlaget.py /
ENTRYPOINT [ "python3", "-u", "./GetDriftlaget.py" ]