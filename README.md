# ZAP Headless Scanner 

This project leverages the ZAP headless scanner along with a FLASK API to allow development users the ability to launch the docker containers and scan it against their deployments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Docker
```

### Deployment

Launch the docker deploy script
> bare version good for fast deployment
> stable version good for more features (not yet needed in the API)

```sh
./app/deploy.sh [version]
```

Ensure the containers have started by running

```sh
docker ps
```


## Authors

* **Nathan Getty** - *Owner* - [GetSec](https://github.com/GetSEc)


## Acknowledgments

* Big thumbs up to the boys at OWASP for creating ZAP

