#!/bin/bash
STABLE="docker pull owasp/zap2docker-stable"
BARE="owasp/zap2docker-bare"
IP_ADDR="127.0.0.1"
FLASK_IMAGE="flask:latest"
ZAP_PORT="1337"
ENV=$1
FLASK_PORT="5000"
function deploy_flask () {
    docker build -t $FLASK_IMAGE .
    docker run  -d -p $FLASK_PORT\:$FLASK_PORT -e "ZAP_URL=http://$ZAP_IP" -e "ZAP_PORT=$ZAP_PORT" $FLASK_IMAGE
}

function deploy_zap () {
    echo "Buidling ZAP ($ENV)"
    if [ "$ENV" == "stable" ]; then
        IMG=$STABLE
        CID=$(docker run -d  -p $ZAP_PORT\:$ZAP_PORT -i $IMG zap.sh -daemon -host '0.0.0.0' -port $ZAP_PORT -config api.addrs.addr.name=.\* -config api.addrs.addr.regex=true -config api.disablekey=true)
    elif [ "$ENV" == "bare" ]; then
        IMG=$BARE
        CID=$(docker run -d -u zap -p $ZAP_PORT\:$ZAP_PORT -i $IMG zap.sh -daemon -host '0.0.0.0' -port $ZAP_PORT  -config api.addrs.addr.name=.\* -config api.addrs.addr.regex=true -config api.disablekey=true)
    else
        echo "Missing param [stable/bare]"
    fi
    ZAP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CID)
}

echo "Currently deploying ZAP"
deploy_zap

# if [[ "$(docker images -q $FLASK_IMAGE 2> /dev/null)" == "" ]]; then
#     echo "Attempting to launch flask with tag $FLASK_IMAGE"
#     deploy_flask
# else
#     echo "[$FLASK_IMAGE] does exist. Will not re-build"
# fi
#echo "Building the FLASK APP"
echo "Launched ZAP: http://0.0.0.0:$ZAP_PORT"
# echo "Succesfully launched flask connected to ZAP: http://$IP_ADDR:$FLASK_PORT"

