# ZAP Headless Scanner 

This project leverages the ZAP headless scanner along with a FLASK API to allow development users the ability to launch the docker containers and scan it against their deployments.

## Getting Started

These instructions will get you a copy of the project and the deployment scripts that deploy the docker images that support the project. 

```
ZapIt
|--> app
|     |----> deploy.sh <-- Used for deploying flask and ZAP images
|--> docs
|     |----> API.md <-- API Documents for the Flask API front end
|--> tests 
      |----> run.py <-- Used for validation once stack is running
|--> app.py <-- Flask API front end
|--> DockerFile <-- Dockerfile for deploying the flask app
|--> requirements.txt <-- Python requirements
|--> README.md     <-- the instructions 
```

### Prerequisites

- Docker

### Deployment

Launch the docker deploy script
> *bare* version good for fast deployment

> *stable* version good for more features (not yet needed in the API)

```sh
./app/deploy.sh [version]
```

Ensure the containers have started by running

```sh
docker ps
```

## Local Development

If you want to run this repo locally, and develop go ahead. Leverage the test cases, ensure that the ZAP_URL and ZAP_PORT are set in the environ, or hardcode them if you wish.

Any pull requests will be reviewed. Please add :D

## Authors

* **Nathan Getty** - *Owner* - [GetSec](https://github.com/GetSEc)


## Acknowledgments

* Big thumbs up to the boys at OWASP for creating ZAP
