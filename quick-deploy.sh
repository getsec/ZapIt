#!/bin/bash
# TODO: Clean this up and document
IMG="owasp/zap2docker-bare"
IP_ADDR="127.0.0.1"
FLASK_IMAGE="flask:latest"
ZAP_PORT="8080"
FLASK_PORT="5000"
ZAP=http://$IP_ADDR:$ZAP_PORT
FLASK=http://$IP_ADDR:$FLASK_PORT
PROFILE=~/.profile
OPTION=$1

# Checks to see if profile is already srcd
if grep -q 'export FLASK=' "$PROFILE"; then
  echo "FLASK Profile already sourced"
else
 
    echo "export FLASK=$FLASK" >> ~/.profile
    . $PROFILE
fi


function deploy_flask () {
    docker build -t $FLASK_IMAGE .
    docker run -d -p $FLASK_PORT\:$FLASK_PORT -e "ZAP_URL=http://$ZAP_IP" -e "ZAP_PORT=$ZAP_PORT" $FLASK_IMAGE
}

function deploy_zap () {
    CID=$(docker run  -d  -p $ZAP_PORT:$ZAP_PORT -i $IMG zap.sh -daemon -host '0.0.0.0' -port $ZAP_PORT -config api.addrs.addr.name=.\* -config api.addrs.addr.regex=true -config api.disablekey=true)
    ZAP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CID)
    echo "ZAP Deployed: http://$ZAP_IP:$ZAP_PORT"
    if grep -q 'export ZAP=' "$PROFILE"; then
        echo "ZAP Profile already sourced"
    else
    
        echo "export ZAP=http://$ZAP_IP:$ZAP_PORT" >> ~/.profile
        . $PROFILE
    fi

 
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
elif [ "$OPTION" = "all" ]; then
     if [[ "$(docker images -q $FLASK_IMAGE 2> /dev/null)" == "" ]]; then
        deploy_flask
    else
        echo "[$FLASK_IMAGE] does exist. Will not re-build"
    fi
    deploy_zap
else
    echo "use flask/zap/all arg"
fi




