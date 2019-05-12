STABLE="docker pull owasp/zap2docker-stable"
BARE="owasp/zap2docker-bare"
IP_ADDR=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2)
PORT="1337"
ENV=$1

echo "Buidling ZAP ($ENV)"
if [ "$ENV" == "stable" ]; then
    IMG=$STABLE
    docker run -d  -p $PORT\:$PORT -i $IMG zap.sh -daemon -host '0.0.0.0' -port $PORT -config api.addrs.addr.name=.\* -config api.addrs.addr.regex=true -config api.disablekey=true
elif [ "$ENV" == "bare" ]; then
    IMG=$BARE
    docker run -d -u zap -p $PORT:$PORT -i $IMG zap.sh -daemon -host '0.0.0.0' -port $PORT  -config api.addrs.addr.name=.\* -config api.addrs.addr.regex=true -config api.disablekey=true
else
    echo "Missing param [stable/bare]"

fi

#echo "Building the FLASK APP"
#docker build -t flask:latest .
#docker run  -d -p 5000:5000 -e "ZAP_URL=http://$IP_ADDR" -e "ZAP_PORT=$PORT" flask:latest
echo "Succesfully launched flask connected to ZAP: http://$IP_ADDR:$PORT"

