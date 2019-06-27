"""
ZAP API Python Wrapper
Development Stage - not fit for production

# * USE CASE!
Data needed from customer
- Target
- Authentication Type
    - Authentication Params
- Backend Infrastructure in our format
    - Web Service   (apache)
    - Web Framework (Tomcat)
    - DB            (mysql, oracle, mssql)
"""

import zapv2
import time
import sys
import uuid




def initialize(target):
    """Used to initialize the scan. Enable all passive scanners
    
    Arguments:
        target {str} -- url: https://example.com
    
    Returns:
        success/failure
    """
    # Sets default user agent
    zap.core.set_option_default_user_agent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    )
    # enables all passive scanners
    zap.pscan.enable_all_scanners()

    open_url = zap.urlopen(target)
    
    # ensures there is actual payload
    if len(open_url) > 1:
        return True
    else:
        return False


def launch_pscan(target):
    # Passive scan just gets data from spider
    id = zap.spider.scan(
        url=target,
        recurse=True
    )
    return id


def create_context(target):
    label = str(uuid.uuid4()).split('-')[0]
    context_name = target.split('//')[1].split('.')[0] + label
    context_id = zap.context.new_context(
        context_name
    )

    # include all technologies
    zap.context.include_all_context_technologies(
        contextname=context_name
    )

    # include target in context
    include_regex = target + '*'
    set_include_regex = zap.context.include_in_context(
        contextname=context_name,
        regex=include_regex
    )
    if set_include_regex == 'OK':
        return context_id, context_name
    else:
        exit('error setting include in context regex')



if __name__ in '__main__':
    target = 'https://wawanesa.com'
    zap = zapv2.ZAPv2(
        proxies={
            'http': 'http://127.0.0.1:8080',
            'https': 'http://127.0.0.1:8080'
        }
    )

    # Initialize and set passive scanner for spider
    if initialize(target) == False:
        sys.exit("Failure to initialize target")
    
    # Launch spider
    launch_pscan(target)
