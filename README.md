## Shared service monitoring

This code is used to help capture health metrics from websites. It can be re-applied to internal sites/webapps to monitor the health of shared services.

#### Setup for monitoring

* Clone git repo to /opt
* Run as a cron job, per requirements. For example:

*/5 * * * * python3 /opt/http_response/src/siteCheck.py > ~/cron.log 2>&1


#### Folder Structure

To be updated


### Known Issues

N/A
