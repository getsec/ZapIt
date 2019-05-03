STABLE="docker pull owasp/zap2docker-stable"
BARE="owasp/zap2docker-bare"
IP_ADDR=$(hostname -I)
PORT="$PORT"
ENV=$1

if [ "$ENV" == "stable" ]; then
    IMG=$STABLE
    docker run -u zap -p $PORT:$PORT \ 
        -i $IMG zap.sh -daemon \ 
        -host $(IP_ADDR) \ 
        -port $PORT \ 
        -config api.addrs.addr.name=.\* \ 
        -config api.addrs.addr.regex=true

elif [ "$ENV" == "bare" ]
    IMG=$BARE
    docker run -u zap -p $PORT:$PORT \ 
        -i $IMG zap.sh -daemon \ 
        -host $(IP_ADDR) \ 
        -port $PORT \ 
        -config api.addrs.addr.name=.\* \ 
        -config api.addrs.addr.regex=true
else   
    echo "Missing param [stable/bare]"

fi



