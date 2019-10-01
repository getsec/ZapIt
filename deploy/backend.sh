#!/bin/bash

# TODO: 

# You can edit these if you want.
IMG="owasp/zap2docker-bare"
IP_ADDR="127.0.0.1"
API_IMAGE="fastapi-zap"
ZAP_PORT="8080"
FAST_NAME="fast-$(date +%s)"
ZAP_NAME="zap-$(date +%s)"
FAST_API_PORT="5000"

# Everything below this runs off the params set above....

PROFILE=~/.profile
OPTION=$1

# Launches the docker container
docker run --name $ZAP_NAME -d -p $ZAP_PORT:$ZAP_PORT \
    -i $IMG zap.sh -daemon \
    -host '0.0.0.0' \
    -port $ZAP_PORT \
    -config api.addrs.addr.name=.\* \
    -config api.addrs.addr.regex=true \
    -config api.disablekey=true 

ZAP_INTERNAL_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $ZAP_NAME)

# Re-Deploy Flask
docker build -t $API_IMAGE .
docker run -d -p 5000:80 --name fast-$(date +%s) \
    -e "ZAP=http://$ZAP_INTERNAL_IP:$ZAP_PORT" \
    -e "ZAPTLS=https://$ZAP_INTERNAL_IP:$ZAP_PORT" \
    $API_IMAGE




echo "Launched ZAP at: "
echo "$IP_ADDR:$ZAP_PORT"

echo "Launched API at:"
echo "$IP_ADDR:$FAST_API_PORT"

echo "Launched API with the following vars"
echo "ZAP=http://$ZAP_INTERNAL_IP:$ZAP_PORT"
echo "ZAPTLS=https://$ZAP_INTERNAL_IP:$ZAP_PORT"
