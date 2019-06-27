#!/bin/bash
IMG="owasp/zap2docker-stable"
IP_ADDR="127.0.0.1"
FLASK_IMAGE="flask:latest"
ZAP_PORT="8080"
FLASK_PORT="5000"


function deploy_flask () {
    docker build -t $FLASK_IMAGE .
    docker run  -d -p $FLASK_PORT\:$FLASK_PORT -e "ZAP_URL=http://$ZAP_IP" -e "ZAP_PORT=$ZAP_PORT" $FLASK_IMAGE
}

function deploy_zap () {
    CID=$(docker run -d  -p $ZAP_PORT:$ZAP_PORT -i $IMG zap.sh -daemon -host '0.0.0.0' -port $ZAP_PORT -config api.addrs.addr.name=.\* -config api.addrs.addr.regex=true -config api.disablekey=true)
    ZAP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CID)
    echo "ZAP Deployed: http://$ZAP_IP:$ZAP_PORT"
}

echo "Currently deploying ZAP"
deploy_zap


