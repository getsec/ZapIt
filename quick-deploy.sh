#!/bin/bash

# TODO: 

# You can edit these if you want.
IMG="owasp/zap2docker-bare"
IP_ADDR="127.0.0.1"
FLASK_IMAGE="flask:latest"
ZAP_PORT="8080"
FLASK_PORT="5000"

# Everything below this runs off the params set above....

FLASK=http://$IP_ADDR:$FLASK_PORT
PROFILE=~/.profile
OPTION=$1

# Launches the docker container
docker run -d -p $ZAP_PORT:$ZAP_PORT \
    -i $IMG zap.sh -daemon \
    -host '0.0.0.0' \
    -port $ZAP_PORT \
    -config api.addrs.addr.name=.\* \
    -config api.addrs.addr.regex=true \
    -config api.disablekey=true
echo "Launched ZAP at: "
echo "$IP_ADDR:$ZAP_PORT"


# Re-Deploy Flask
docker build -t $FLASK_IMAGE .
docker run -d -p $FLASK_PORT\:$FLASK_PORT \
    -e "ZAP=http://$IP_ADDR:$ZAP_PORT" \
    -e "ZAPTLS=https://$IP_ADDR:$ZAP_PORT" \
    $FLASK_IMAGE

echo "Launched flask with the following vars"
echo "ZAP=http://$IP_ADDR:$ZAP_PORT"
echo "ZAPTLS=https://$IP_ADDR:$ZAP_PORT"

# # Checks to see if profile is already srcd
# if grep -q 'export FLASK=' "$PROFILE"; then
#   echo "FLASK Profile already sourced - updating"
#   # Since it already exists in the file, we replace it with the new values
#   sed -e "s|export FLASK.*|export FLASK=$FLASK|g" -i $PROFILE
#   . $PROFILE
# else
#     echo "export FLASK=$FLASK" >> ~/.profile
#     . $PROFILE    
# fi


# function deploy_flask () {
#     docker build -t $FLASK_IMAGE .
#     docker run -d -p $FLASK_PORT\:$FLASK_PORT  $FLASK_IMAGE
#     # -e "ZAP_URL=$ZAP" -e "ZAP_PORT=$ZAP_PORT" <<<< This goes above...
#     ZAP_URL=$ZAP
#     sleep 2
# }

# function deploy_zap () {
#     CID=$(docker run  -d  -p $ZAP_PORT:$ZAP_PORT -i $IMG zap.sh -daemon -host '0.0.0.0' -port $ZAP_PORT -config api.addrs.addr.name=.\* -config api.addrs.addr.regex=true -config api.disablekey=true)
#     ZAP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CID)
#     echo "ZAP Deployed: http://localhost:$ZAP_PORT"
#     if grep -q 'export ZAP=' "$PROFILE"; then
#         echo "ZAP Profile already sourced"
#         # Since it already exists in the file, we replace it with the new values
#         sed -e "s|export ZAP.*|export ZAP=http://localhost:$ZAP_PORT|g" -i $PROFILE
#         . $PROFILE
#     else
#         echo "export ZAP=http://localhost:$ZAP_PORT" >> ~/.profile
#         . $PROFILE
#     fi

#     if grep -q 'export ZAPTLS=' "$PROFILE"; then
#         echo "ZAPTLS Profile already sourced"
#         # Since it already exists in the file, we replace it with the new values
#         sed -e "s|export ZAPTLS.*|export ZAPTLS=$ZAPTLS|g" -i $PROFILE
#         . $PROFILE
#     else
#         echo "export ZAPTLS=https://$ZAP_IP:$ZAP_PORT" >> ~/.profile
#         . $PROFILE
#     fi
# }




# if [ "$OPTION" = "flask" ]; then
#     if [[ "$(docker images -q $FLASK_IMAGE 2> /dev/null)" == "" ]]; then
#         deploy_flask
#     else
#         echo "[$FLASK_IMAGE] does exist. Will not re-build"
#     fi
# elif [ "$OPTION" = "flaskl" ]; then
#     export FLASK_APP=app.py
#     export FLASK_ENV=development

#     flask run
# elif [ "$OPTION" = "zap" ]; then
#     deploy_zap
# elif [ "$OPTION" = "all" ]; then
#     deploy_zap

#     if [[ "$(docker images -q $FLASK_IMAGE 2> /dev/null)" == "" ]]; then
#         deploy_flask
#     else
#         echo "[$FLASK_IMAGE] does exist. Will not re-build"
#     fi
    
# else
#     echo "use flask/zap/all arg"
# fi
