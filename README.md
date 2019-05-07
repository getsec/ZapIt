# ZAP Headless Scanner 

This project leverages the ZAP headless scanner along with a FLASK API to allow development users the ability to launch the docker containers and scan it against their deployments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Python 3
- Docker
- Python Libraries
    - flask
    - requests


```
Flask==1.0.2
requests==2.21.0
```

### Installing

First install the python libraries

```sh
pip install -r requirements.txt
```

Launch the docker deploy script

```sh
./deploy.sh
```

Ensure the containers have started by running

```sh
docker ps
```


## Authors

* **Nathan Getty** - *Owner* - [GetSec](https://github.com/GetSEc)


## Acknowledgments

* Big thumbs up to the boys at OWASP for creating ZAP
