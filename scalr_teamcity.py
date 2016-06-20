"""
Python script to start a TeamCity job with parameters.
 + based on scalr.py
   - https://github.com/micharris/taurus-test/blob/master/scalr.py

TODO:
   - add argparse and include sane defaults
   - review request response code (200 vs 4xx/5xx)
   - verify job is submitted
   - verify input before post
"""

import sys
import urllib

# TeamCity Server URL
# + http://API_KEY:SECRET_KEY@API_URL/
API_KEY = sys.argv[1]
SECRET_KEY = sys.argv[2]
API_URL = sys.argv[3]

# Parameters for TeamCity Job
# + "httpAuth/action.html?add2Queue=JOB_NAME
# + "&JOB_PARAM" - list of key value pairs (similar to below)
# + "&name=PROJECT_ID&value=PROJECT_ID"
PROJECT_ID = sys.argv[4]
JOB_NAME = sys.argv[5]
JOB_PARAM = sys.argv[6]


def main(api_key, secret_key, api_url, project_id, job_name, job_param):
    api_path = "httpAuth/action.html"
    api_param = "?add2Queue=%s&%s&name=PROJECT_ID&value=%s" % (job_name,
                                                               job_param,
                                                               project_id)
    api_get = "http://%s:%s@%s/%s%s" % (api_key, secret_key,
                                        api_url, api_path, api_param)
    print (api_get)
    req = urllib.urlopen(api_get)
    return req.read()


if __name__ == "__main__":
    print main(API_KEY, SECRET_KEY, API_URL, PROJECT_ID, JOB_NAME, JOB_PARAM)
