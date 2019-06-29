#!/bin/bash
IMG="owasp/zap2docker-stable"
IP_ADDR="127.0.0.1"
FLASK_IMAGE="flask:latest"
ZAP_PORT="8080"
FLASK_PORT="5000"
OPTION=$1

function deploy_flask () {
    docker build -t $FLASK_IMAGE .
    docker run  -d -p $FLASK_PORT\:$FLASK_PORT -e "ZAP_URL=http://$ZAP_IP" -e "ZAP_PORT=$ZAP_PORT" $FLASK_IMAGE
}

function deploy_zap () {
    CID=$(docker run -d  -p $ZAP_PORT:$ZAP_PORT -i $IMG zap.sh -daemon -host '0.0.0.0' -port $ZAP_PORT -config api.addrs.addr.name=.\* -config api.addrs.addr.regex=true -config api.disablekey=true)
    ZAP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CID)
    echo "ZAP Deployed: http://$ZAP_IP:$ZAP_PORT"
}




if [ "$OPTION" = "flask" ]; then
    if [[ "$(docker images -q $FLASK_IMAGE 2> /dev/null)" == "" ]]; then
        deploy_flask
    else
        echo "[$FLASK_IMAGE] does exist. Will not re-build"
    fi
elif [ "$OPTION" = "flaskl" ]; then
    export FLASK_APP=app.py
    export FLASK_ENV=development

    flask run
elif [ "$OPTION" = "zap" ]; then
    deploy_zap
elif [ "$OPION" = "all" ]; then
     if [[ "$(docker images -q $FLASK_IMAGE 2> /dev/null)" == "" ]]; then
        deploy_flask
    else
        echo "[$FLASK_IMAGE] does exist. Will not re-build"
    fi
    deploy_zap
else
    echo "use flask/zap/all arg"
fi




