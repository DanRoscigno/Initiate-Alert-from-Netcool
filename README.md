# Initiate-Alert-from-Netcool
Tooling to allow users to initiate alerts via Alert Notification Service or PagerDuty

Here is the flow I am starting with:

 - Customer Care (CSR) or SRE determines that there is a Sev One need for DevOps to concentrate on an issue.
 - An incident number is assigned in the Customer Care system
 - Customer Care uses a tool and inputs the following information:
      - Incident Number
      - Customer name
      - Customer ENV (some type of customer assigned identifier, maybe just 'Prod' or 'Dev')
      - Issue description
      - DevOps team needed (a particular application, or the Network team)
 - A *SWAT tracking event* is created in the Netcool ObjectServer with the above information
 - The SRE(s) on call and the CSRs will be notified by the paging service
 - The SRE will use a tool associated with the *SWAT tracking event* to:
      - Create a Slack channel for the SWAT
      - Notify the DevOps team of the SWAT and give them the Slack channel URL
      - Send the SWAT Close page when the service is available for the impacted customer





This is the curl from the docs:

curl -X POST -v -u root:*pass* \
     -H "Accept:application/json" \
     -H "Content-Type: application/json" \
     -d @event-template.json \
     http://localhost:8080/objectserver/restapi/alerts/status
