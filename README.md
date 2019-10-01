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
