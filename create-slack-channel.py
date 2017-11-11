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


r = requests.post(URI, data={'token': token, 'name': 'dan-test-6'})
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
        
