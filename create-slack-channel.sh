#!/bin/sh
#

#######################################


help() {
	echo "usage: `basename $1` [options] [name=value]..."
	echo
	echo "where options can be:"
	echo
	echo "	-help		Print this help text"
	echo "	-token		Required: <Slack API token>"
	echo "	-channelname	Optional: channel name "
	echo "	-validate	Optional: Fail on a bad channel name, leave unset to allow Slack to fix the name"
	echo "	-pretty		Optional: Pretty print the response, leave unset for raw output"
	echo
	exit 0
}

CHANNELNAME=`date --utc +sre-%Y%m%d-%H%M`
SLACKTOKEN=""
CHANNELPURPOSE=""
VALIDATECHANNELNAME="false"
PRETTYPRINT="0"

while [ $# -gt 0 ]; do
	case "$1" in
	-channelname)
		if [ $# -lt 2 ]; then
			err "$1 option requires an argument"
		fi
		shift	
		CHANNELNAME="$1"
		;;
	-token)
		if [ $# -lt 2 ]; then
			err "$1 option requires an argument"
		fi
		shift	
		SLACKTOKEN="$1"
		;;
	-validate)
		VALIDATECHANNELNAME="true"
		;;
	-pretty)
		PRETTYPRINT="1"
		;;
	-he*|-H|-?)
		help $0 2>&1
		;;
	-*)
		err "unknown option $1"
		;;
	*)
	esac
	shift
done

if [ "$SLACKTOKEN" = "" ]; then
	err "-token is required"
fi


DATA="token="$SLACKTOKEN
DATA=$DATA"&name="$CHANNELNAME
DATA=$DATA"&""validate="$VALIDATECHANNELNAME
DATA=$DATA"&""pretty="$PRETTYPRINT

URI=https://slack.com/api/channels.create



curl -s -X POST --header 'Content-Type: application/x-www-form-urlencoded' -d "${DATA}" -w "\n%{http_code}\n" ${URI}
response_text=$(curl -s -X POST --header 'Content-Type: application/x-www-form-urlencoded' -d "${DATA}" -w "\n%{http_code}\n" ${URI} | awk '/"name":/{print $2}')
echo $response_text

response_int=$?
if test "$response_int" != "0"; then
   logger "nco_slack_channel: the curl command failed with: $response_int"
else
   logger "nco_slack_channel: succeeded with: $response_int"
fi
