#coding:utf-8
import datetime
import urllib
import base64
import hmac
import hashlib
import sys

SCALR_API_KEY = sys.argv[1]
SCALR_SECRET_KEY = sys.argv[2]

API_URL = sys.argv[3]
API_VERSION = '2.3.0'
API_AUTH_VERSION =  '3'

datadog = sys.argv[4]
projectid = sys.argv[5]

API_ACTION = "ScriptExecute"


def main(key_id, secret_key):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    params = {
        "Action": API_ACTION,
        "Version": API_VERSION,
        "AuthVersion": API_AUTH_VERSION,
        "EnvID": 6,
        "FarmID": 1988,
        "FarmRoleID": 6163,
        "ScriptID": 148,
        "Timeout": 120,
        "Async": 1,
        "Timestamp": timestamp,
        "KeyID": key_id,
        "ConfigVariables[datadog_servers]": datadog
        "ConfigVariables[projectid]": projectid
        "Signature":  base64.b64encode(hmac.new(secret_key, ":".join([API_ACTION, key_id, timestamp]), hashlib.sha256).digest()),
    }
    urlparams = "Action="+API_ACTION+"&Version="+API_VERSION+"AuthVersion="+API_AUTH_VERSION+"EnvID=6&FarmID=2263&ScriptID=148&Timeout=120&Async=1&Timestamp="+timestamp+"KeyID="+key_id+"&ConfigVariables[datadog_servers]="+datadog+"&ConfigVariables[projectid]"+projectid+"&Signature="+base64.b64encode(hmac.new(secret_key, ":".join([API_ACTION, key_id, timestamp]), hashlib.sha256).digest())

    req = urllib.urlopen(API_URL, urlparams)

    return req.read()


if __name__ == "__main__":
    print main(SCALR_API_KEY, SCALR_SECRET_KEY)