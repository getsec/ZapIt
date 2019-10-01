# ZapIt - Vulnerability Scanner

This project leverages the ZAP headless scanner along with an API to allow development users the ability to launch the docker containers and scan it against their web applications in a easy scalale fashion

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Docker
- Python 3.6 +
- Python Dependencies

```sh
pip install -r requirements.txt --user
```

### Installing
A step by step series of examples that tell you how to get a development env running

Clone this repo.

Launch the deploy script.

``` sh
./backend.sh
```


## Running the tests

Custom tests developed to run an example domain through a rudimentary test.

``` sh
python tests/run.py
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
