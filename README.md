# SG-Agent

SG-Agent gets your public IP depending on configure time (default 5 minutes) and updates all aws security groups rules and ports in different regions.
The Agent checks the Security Groups and revokes all rules then adds the new public ip and ports. 
This is useful when using EC2, Redshift and RDS from Public ip that changes so often. 

You need to configure AWS access key and secret key by this link https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html 

## Requirements

* python3
* pip


### Run

clone the repo

    $ git clone https://github.com/maradwan/sg-agent.git

### Install the dependencies:
   
    $ cd sg-agent
    $ pip install -r requirements.txt

### Copy sg-agent.service to /etc/systemd/system/
    
    $ cp sg-agent.service /etc/systemd/system/
    $ cp sg-agent.py /usr/bin/
    $ cp sg-agent-config.yaml /etc/
    
### Edit sg-agent-config.yaml to define which security, port and region

    $ vim /etc/sg-agent-config.yaml
    
### Edit the service file to configure the time (time in seconds, default 5 minutes) and add your home user to <HOME USER> ex: ubuntu  

    $ vim /etc/systemd/system/sg-agent.service
   
### Reload the config and start the service

    $ systemctl daemon-reload
    $ service sg-agent start
   
