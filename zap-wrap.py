"""
ZAP API Python Wrapper
Development Stage - not fit for production
"""

import zapv2
import time
from pprint import pprint
import uuid
import urllib.parse


def register_target(target):
    open_url = zap.urlopen(target)
    return open_url

# Create new context
def create_context():
    label = str(uuid.uuid4()).split('-')[0]
    context_name = target.split('//')[1].split('.')[0] + label
    context_id = zap.context.new_context(
        context_name
    )
    return context_id

# form based auth example
def set_authentication(target, login_uri, context_id, 
                       login_request_data, login_indicator):
    """Sets form based authentication
    
    Arguments:
        target {str} --this is set
        login_uri {str} -- uri for the login page (login.html)
        context_id {str} -- context id for sesions
        login_request_data {str} -- unparsed url data (username=x&password=y&submit=submit)
        login_indicator {str} -- regex capture to ensure succesful
    """
    login_request_data = urllib.parse.quote(login_request_data)
    form_auth_cfg = f"loginUrl={target}/{login_uri}&"
    form_auth_cfg += f"loginRequestData={login_request_data}"

    auth = zap.authentication.set_authentication_method(
        contextid=context_id,
        authmethodname='formBasedAuthentication',
        authmethodconfigparams=form_auth_cfg
    )
    if auth == "OK":
        return auth
    else:
        return "Authentication parameters failed"
    # TODO: Set login indicator



# Launch spider
def launch_spider(target):
    scanid = zap.spider.scan(target)
    while (int(zap.spider.status(scanid)) < 100):
        print('Spider progress %: ' + zap.spider.status(scanid))
        time.sleep(2)
    return scanid

def launch_active_scan(target):
    scanid = zap.ascan.scan(target)
    while (int(zap.ascan.status(scanid)) < 100):
        print('Scan progress %: ' + zap.ascan.status(scanid))
        time.sleep(5)
    return scanid


if __name__ in '__main__':
    target = 'https://example.com'
    zap.urlopen(target)
    zap = zapv2.ZAPv2(
        proxies={
            'http': 'http://127.0.0.1:1337',
            'https': 'http://127.0.0.1:1337'
        }
    )
    # TODO: ensure the target is part of this
    context_id = create_context()
    launch_spider(target)
    launch_active_scan(target)
    login_request_data = "username=ngetty&password=mypass123&submit=submit"
    login_indicator = "*succsesful login*"

    auth = set_authentication(target, "login.html", context_id, login_request_data, login_indicator)