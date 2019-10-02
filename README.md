# ZapIt - Vulnerability Scanner

This project leverages the ZAP headless scanner along with an API to allow development users the ability to launch the docker containers and scan it against their web applications in a easy scalable fashion


### Prerequisites

- Docker
- Python 3.6 +
- Python Dependencies

```sh
pip install -r requirements.txt --user
```

### Building the backend
A step by step series of examples that tell you how to get a development env running

1. Clone this repo.
2. Deploy the backend infrastructure
    ``` sh
    ./backend.sh
    ```

### Scanning 

You can scan your environment by leveraging ZAP directly, or by using the prebuilt scan script for quick and easy results.

``` sh
python scan.py [http|https]://full.example.domain.com
```
> Dont worry about redirects, there is logic in the helper files that handle that, so sites that convert "example.com" > "www.example.com" are handled.

### Take it out for a spin
Here is a quick example of how you can scan your site and what the results look like, keep in mind this will be changing with new releases
```
$ python3 scan.py https://ngetty.me

    _____          ___ _.
   |__  /__ _ _ __|_ _| |_
     / // _` | '_ \| || __|
    / /| (_| | |_) | || |_
   /____\__,_| .__/___|\__|
             |_|
  OWASP ZAP CI/CD TESTING TOOL
 ** Actively in development. **

ScanID 7
Active Scan Progress: 0
Active Scan Progress: 0
Active Scan Progress: 36
Active Scan Progress: 38
Active Scan Progress: 63
Active Scan Progress: 89


TOTAL RESULTS


[{'alert': 'Directory Browsing',
  'evidence': '',
  'method': 'GET',
  'param': '',
  'risk': 'Medium',
  'solution': 'Disable directory browsing.  If this is required, make sure the '
              'listed files does not induce risks.',
  'url': 'https://ngetty.me/js/'},
 {'alert': 'Cross-Domain JavaScript Source File Inclusion',
  'evidence': '<script '
              'src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBVWaKrjvy3MaE7SQ74_uJiULgl1JY0H2s&sensor=false"></script>',
  'method': 'GET',
  'param': 'https://maps.googleapis.com/maps/api/js?key',
  'risk': 'Low',
  'solution': 'Ensure JavaScript source files are loaded from only trusted '
              "sources, and the sources can't be controlled by end users of "
              'the application.',
  'url': 'https://ngetty.me/portfolio.html'}]
(venv) getty@getty:~/ZapIt$

```

## Built With

* [FastAPI](https://github.com/tiangolo/fastapi) - Quick as hell
* [OWASP ZAP](https://github.com/zaproxy/zaproxy/wiki/Docker) - Scanning tool
* [Docker](https://docker.com) - Used for containterized deployment

## Contributing

Send in a PR and I'll review it :)

## Authors

**Nathan Getty** - *Owner* - [GetSec](https://github.com/GetSec)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Big shoutout to all the OWASP team for developing ZAP
