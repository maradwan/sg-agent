import boto3
import yaml
import requests
from datetime import datetime
from socket import gethostname

with open('sg-agent-config.yaml') as f:
    sg = yaml.safe_load(f)

aws_sg = sg['AWS']

HostName = gethostname()

LastUpdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Get Your Public IP
get_ip =  requests.get('http://ifconfig.me')
if get_ip.status_code != 200:
    get_ip = requests.get('http://ipinfo.io/ip')
elif get_ip.status_code != 200:
    get_ip = requests.get('http://api.ipify.org')

# Adding Rules to SG
def aws_sg_add_rules(sg_id,port,region):
    ec2 = boto3.client('ec2',region_name=region)
    return ec2.authorize_security_group_ingress(
    GroupId = sg_id,
    IpPermissions = [
        {'IpProtocol': 'tcp',
        'FromPort': port,
        'ToPort': port,
        'IpRanges': [
                {
                    'CidrIp': get_ip.text + '/32',
                    'Description': 'SG-Agent Hostname: {} LastUpdate: {}'.format(HostName,LastUpdate)
                },
            ]},
        ])

# Remove All Old Rules from SG
def aws_sg_revoke(sg_id,IpPermissions,region):
    ec2 = boto3.client('ec2',region_name=region)
    return ec2.revoke_security_group_ingress(GroupId=sg_id, IpPermissions=IpPermissions)

# GET SG Info
def aws_sg_check(sg_id,region):
    ec2 = boto3.client('ec2',region_name=region)
    response = ec2.describe_security_groups(GroupIds=[sg_id])
    return response


for i in range(len(aws_sg['Resources'])):
    sg_id = aws_sg['Resources']['SG'+ str(i+1)]['SG_ID']
    region = aws_sg['Resources']['SG'+ str(i+1)]['REGION']

    get_sg_info = aws_sg_check(sg_id,region)
    IpPermissions = get_sg_info['SecurityGroups'][0]['IpPermissions']

    try:
        if get_sg_info['SecurityGroups'][0]['IpPermissions']:
            aws_sg_revoke(sg_id, IpPermissions, region)
    except botocore.exceptions.ClientError as error:
        raise error

    for j in range(len(aws_sg['Resources']['SG'+ str(i+1)]['PORTS'])):
        port = aws_sg['Resources']['SG'+ str(i+1)]['PORTS'][j]

        aws_sg_add_rules(sg_id,port,region)
