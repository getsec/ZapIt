import urllib.parse
from requests import get
import sys


def encode(target):
    enc_s = urllib.parse.quote_plus(target)
    return enc_s


def ensure_host_up(base_url):
    u = get(base_url)
    if u.status_code != 200:
        sys.exit(f"Non-200 status code at: {base_url}")
    else:
        print("Continuing with stuff")
    return u


def spider(base_url, encoded_target):  
    url = f"{base_url}/JSON/spider/action/scan/?zapapiformat=JSON&"
    url += f"formMethod=GET&url={encoded_target}&maxChildren=5&recurse=True"

    g = get(url)
    print(g)

if __name__ == "__main__":
    proxy_host = 'http://172.17.0.1'
    proxy_port = '8080'
    target = 'https://google.ca'
    encoded_target = encode(target)
    base_url = f'{proxy_host}:{proxy_port}'
    spider(base_url, encoded_target)

