#!/bin/bash

IMG="owasp/zap2docker-bare" # dont touch this one tho
IP_ADDR="127.0.0.1"  # or this one

# You can edit these if you want.
API_IMAGE="fastapi-zap"
FAST_NAME="fast-$(date +%s)"
ZAP_NAME="zap-$(date +%s)"
FAST_API_PORT="5000"
ZAP_PORT="8080"

# Everything below this runs off the params set above....
# Please dont make changes to below
echo "##########################################"
echo "# Launching ZapIt Backend Infrastructure #"
echo "##########################################".

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


printf "\n\n Looks like we've launched. See details below\n"
printf "\tLaunched ZAP at: $IP_ADDR:$ZAP_PORT\n"
printf "\tLaunched API at: $IP_ADDR:$FAST_API_PORT"

printf "\n Launched API with the following vars\n"
printf "\tZAP=http://$ZAP_INTERNAL_IP:$ZAP_PORT\n"
printf "\tZAPTLS=https://$ZAP_INTERNAL_IP:$ZAP_PORT\n"
