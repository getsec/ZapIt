from os import environ
from requests import get, post



def test_internet_access():
    r = get("https://google.ca", verify=False)
    assert r.ok == 200-399, "Should be 200"

