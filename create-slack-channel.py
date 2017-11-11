#!/opt/IBM/netcool/python27/bin/python
import requests
import json
import sys

token = 'xoxp-4511607439-197777274292-215108860375-a61999c82beae8a29ed58c02c1551c2b'
URI = 'https://slack.com/api/channels.create'


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
   
