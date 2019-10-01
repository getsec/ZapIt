from requests import get
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def get_redirect_url(url):
    """Takes in url, spits out redirect

    Arguments:
        url {str} -- requested url

    Returns:
        [str] -- url 302 redirect
    """
    r = get(url, verify=False)
    return r.url