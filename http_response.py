#!/usr/bin/env python3

import requests
import yaml
import pymsteams
import json
import boto3

#If for some reason this script is run with Python 2, the following line should stop errors:

try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse

# 1 :

def getyamlkey(keyValue):
    
    with open('/opt/http_response/src/config.yml', 'r') as file2:
            try:
                yamlKeys = yaml.load(file2)[keyValue]
                return yamlKeys
            except Exception as e:
                print("Error in configuration file"), e

#Tidies up hostnames & converts HTTP responses to 0 (good) or 1 (not good) then sends to CloudWatch. "Elapsed" is elapsed.total_seconds from #3/ retrieveStatus :

def sendToCloudWatch(teams, url, elapsed):

        statusCode = teams
        statusCodePlain = teams
        respTime = elapsed
        if statusCodePlain == 200:
            statusCodePlain = 0
        elif statusCodePlain != 200:
            statusCodePlain = 1
			
        siteCheckedPlain = url
        parser = urlparse(siteCheckedPlain)
        host = str(parser.hostname)
        hostName = json.dumps(host, default=lambda o: o.__dict__)
        hostName = hostName.replace('\"', '')
		
        print('Details: \n', '\n Hostname: ', hostName, '\n RespTime: ', respTime, '\n statusCodePlain:', statusCodePlain, '\n statusCode: ',  statusCode, '\n siteCheckedPlain: ',  siteCheckedPlain, '\n')
		
        upDownCloudWatch = boto3.client('cloudwatch')

        upDownCloudWatch.put_metric_data(
            MetricData=[
                {
                    'MetricName': 'StatusCode',
                    'Dimensions': [
                        {
                            'Name': 'Service',
                            'Value': hostName
                        },
                    ],  
                    'Unit': 'None',
                    'Value': statusCodePlain
                },
            ],
            Namespace= 'ISU' 
        )

        respTimeCloudWatch = boto3.client('cloudwatch')

        respTimeCloudWatch.put_metric_data(
            MetricData=[
                {
                    'MetricName': 'ResponseTime',
                    'Dimensions': [
                        {
                            'Name': 'Service',
                            'Value': hostName
                        },
                    ],  
                    'Unit': 'None',
                    'Value': respTime
                },
            ],
            Namespace= 'ISU' 
        )

#Sends the data to Teams - failsafe in case Grafana goes to sleep with the fishes:

def sendToTeams(teams, url):
        teamsWebHook = getyamlkey("webhook")
        myTeamsMessage = pymsteams.connectorcard(teamsWebHook)

        print(teams, url)
        myTeamsMessage.text("The following URL: %s -- has returned HTTP status code %s" % (url, teams))
        myTeamsMessage.send()



# 3 :

def retrieveStatus(url):

    resp = requests.get(url)
    resp2 = resp.elapsed.total_seconds()
    # To test functionality, set res.status_code to != 201:
    sendToCloudWatch(resp.status_code, url, resp2)
    
    if resp.status_code != 200:
        sendToTeams(resp.status_code, url)        
    return resp.status_code, resp2



# 2 :

def main():

        urls = getyamlkey('apps')
        for x in urls:
            retrieveStatus(x)


if __name__ == '__main__': main()
