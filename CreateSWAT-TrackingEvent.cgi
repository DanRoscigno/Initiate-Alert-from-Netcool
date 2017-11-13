#!/opt/IBM/netcool/python27/bin/python
import cgitb
cgitb.enable()
print "Content-type: text/html"
print

print """
<html>

<head><title>Post to AlertNotification</title></head>

<body>

  <h3>Post to AlertNotification </h3>
<br><br>
  <pre>
"""

import json
import requests

"""
Put your OMNIbus REST API uri, username and pass into a config file
AlertNotification.ini in this format:

[AGG_V]
URI: http://localhost:8080/objectserver/restapi/alerts/status
username: root
password: abcdef

"""

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("/opt/IBM/netcool/gui/omnibus_webgui/etc/cgi-bin/AlertNotification.ini")

import os, sys
from cgi import escape

keys = os.environ.keys()

import urlparse
SWAT_info = {}
SWAT_info = dict(urlparse.parse_qsl(os.environ['QUERY_STRING']))

"""
This gives me these keys:
    Key				          Description
  Service           Impacted service
  SWAT_issue        Issue reported by customer
  SWAT_customer     Customer name and environment
  WEBTOP_USER       Username in Netcool
"""

import time
session        = SWAT_info['SWAT_session']
issue          = SWAT_info['SWAT_issue']
customer       = SWAT_info['SWAT_customer']
Service        = SWAT_info['Service']
Identifier     = 'Initiate SWAT Tool ' + str(time.time()) + ' ' + Service
Where          = customer + ' ' + SWAT_info['SWAT_environment']
Summary        = 'Customer: ' + customer + ' Env: ' + SWAT_info['SWAT_environment'] 
TTNumber       = session
Severity       = 5
Type           = 1
Source         = 'Initiate SWAT Tool'

# In the HTML form that the user fills out I display the current GMT time so that they can edit it 
# to match the time that the customer reported the issue (my expectation is that the CSR will see 
# that the customer called three minutes ago and change a displayed time of 2:55 to 2:52).
#
# These next few lines convert the time sent over in the form back into epoch seconds so that I can 
# time as FirstOccurrence and LastOccurrence of the event.

date_time = SWAT_info['SWAT_TimeRaised']
pattern = '%a, %d %b %Y %H:%M:%S %Z'
os.environ['TZ']='UTC'
epoch = int(time.mktime(time.strptime(date_time, pattern)))
LastOccurrence = epoch

# Up top we read the config, now we will lookup the username and password for Alert Notification
URI        = Config.get('AGG_V', 'URI')
username   = Config.get('AGG_V', 'username')
password   = Config.get('AGG_V', 'password')

event_data = {
   "rowset":{
      "coldesc":[
         {
            "type":"string",
            "name":"Identifier"
         },
         {
            "type":"string",
            "name":"Node"
         },
         {
            "type":"string",
            "name":"AlertKey"
         },
         {
            "type":"integer",
            "name":"Severity"
         },
         {
            "type":"integer",
            "name":"Type"
         },
         {
            "type":"string",
            "name":"Manager"
         },
         {
            "type":"string",
            "name":"Summary"
         },
         {
            "type":"string",
            "name":"application"
         },
         {
            "type":"string",
            "name":"TTNumber"
         },
         {
            "type":"utc",
            "name":"FirstOccurrence"
         },
         {
            "type":"utc",
            "name":"LastOccurrence"
         },
         {
            "type":"integer",
            "name":"OwnerUID"
         },
         {
            "type":"integer",
            "name":"OwnerGID"
         }
      ],
      "rows":[
         {
            "Identifier"     : "%s" % Identifier,
            "Node"           : "localhost",
            "AlertKey"       : "InitiateSWAT",
            "Severity"       : Severity,
            "Type"           : Type,
            "Manager"        : "Initiate SWAT Tool",
            "Summary"        : "%s" % Summary,
            "application"    : "%s" % Service,
            "TTNumber"       : "%s" % TTNumber,
            "FirstOccurrence": LastOccurrence,
            "LastOccurrence" : LastOccurrence,
            "OwnerUID"       : 0,
            "OwnerGID"       : 0
         }
      ]
   }
}

print 'This is what was sent to OMNIbus:'
print json.dumps(event_data, sort_keys=False, indent=4, separators=(',', ': '))
print '</pre>'

omnibusResponse = requests.post(
    URI, auth=(username,password), json=event_data
)


if omnibusResponse.status_code != 201:
    raise ValueError(
        'There was an error (%s) during posting the message to Alert Notification, the response is:\n%s'
        % (omnibusResponse.status_code, omnibusResponse.text)
    )
else:
    print "Successfully posted to OMNIbus"

print """

<br>
<b>Note: Please close this tab before initiating another SWAT.</b>

</body>

</html>
"""
