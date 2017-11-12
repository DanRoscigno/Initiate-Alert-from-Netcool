#!/opt/IBM/netcool/python27/bin/python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import time

print "Content-type: text/html"
print

print """
<html>

<head><title>Create Slack Channel</title></head>

<body>

"""

import os, sys
keys = os.environ.keys()
keys.sort()
#for k in keys:
    #print "%s\t%s" % (cgi.escape(k), cgi.escape(os.environ[k]))

# Extract the information we need from the os.environ() key value pairs.
# The fields passed in from Netcool (Node, Summary, etc., are in
# the QUERY_STRING, which looks like this:
# QUERY_STRING	datasource=OMNIBUS&$selected_rows.NodeAlias=foo-demo&$selected_rows.AlertKey=CSI_ISMBadWebSiteFatal&$selected_rows.application=NC&$selected_rows.Severity=5&$selected_rows.ITMDisplayItem=nc:foo-demo/Unity&CONVERSION.$selected_rows.Severity=Critical&$selected_rows.Summary=nc:foo-demo/Unity&$selected_rows.Node=foo-demo

alert_string = os.environ['QUERY_STRING'];

"""
Given an alert_string like so:
  datasource=OMNIBUS&$selected_rows.NodeAlias=foo-demo&$selected_rows.AlertKey=CSI_ISMBadWebSiteFatal
1) split the string into "<key>=<value>" chunks: s.split('&')
2) split each chunk into "<key> ", " <value>" pairs: item.split('=')
"""

alert_kvpairs = dict(item.split('=') for item in alert_string.split('&'))

"""
This gives me these keys:
    Key                              Description
 $selected_rows.AlertKey             AlertKey
 $selected_rows.NodeAlias            IP Address
 $selected_rows.Summary	             Summary
 $selected_rows.ITMDisplayItem	     Alternate Summary
 $selected_rows.application          Ops group (lookup for slack channel
 CONVERSION.$selected_rows.Severity  Severity String
 $selected_rows.Node                 Hostname
 $selected_rows.LastOccurrence       Time of most recent alert
"""

session        = alert_kvpairs['$selected_rows.TTNumber']
identifier     = alert_kvpairs['$selected_rows.Identifier']
application    = alert_kvpairs['$selected_rows.application']
lastoccurrence = alert_kvpairs['$selected_rows.LastOccurrence']

print """
  <input type="submit" value="Send to Slack">
  </form>
  <pre>
  </pre>
</body>

</html>
"""
# % cgi.escape(message)
#!/opt/IBM/netcool/python27/bin/python
import requests
import json
import sys

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("/opt/IBM/netcool/gui/omnibus_webgui/etc/cgi-bin/AlertNotification.ini")

# Up top we read the config, now we will lookup the username and password for Alert Notification
token = Config.get('SLACKTEAM', 'token')
URI   = Config.get('SLACKTEAM', 'URI')

channel = 'sre-' + session + '-' + application

r = requests.post(URI, data={'token': token, 'name': channel})
r.raise_for_status()
if not r.ok:
    raise ValueError(
        'There was an http error (%s) during creating the channel, the response is:\n%s'
        % (r.status_code, r.text)
    )
    sys.exit(1)
else:
    print "http POST OK"
    resp_dict = json.loads(r.text)
    if not resp_dict['ok']:
        print 'The channel creation failed, the error message is:\n%s' % resp_dict['error']
    else:
        print 'Channel creation OK'
        print 'Channel name: %s' % resp_dict["channel"]["name_normalized"]
        print 'Channel ID: %s' % resp_dict["channel"]["id"]
   

