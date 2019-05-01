#!/bin/bash 

ensure_host_up() {
    CHECK=$(curl $PROXY_HOST:$PROXY_PORT -s --verbose 2>&1 | grep 200)
    if [ $? == 0 ]; then
        echo "Confirmed ZAP is running: $CHECK"
    else
        echo "zap is not running" 
        echo "How to run ZAP:"
        launch_zap
        exit 255
    fi
}

spider_host (){
    SPIDER_URL="http://$PROXY_HOST:$PROXY_PORT/JSON/spider/action/scan/?zapapiformat=JSON&formMethod=GET&url=https%3A%2F%2Fwww.$TARGET&maxChildren=10&recurse=True&contextName=&subtreeOnly="
    HOSTS=$(curl -s $SPIDER_URL 2>&1)
    SCAN_ID=$(curl -s $SPIDER_URL 2>&1 |  jq .scan | sed 's/"//g')
    echo "Launching Scan..."
    echo $PROXY_HOSTS | jq
    sleep 10

    SCAN_TOTAL=0
    while [  $SCAN_TOTAL -lt 98 ]; do
        SCAN_STATUS="http://$PROXY_HOST:$PROXY_PORT/JSON/spider/view/status/?zapapiformat=JSON&formMethod=GET&scanId=$SCAN_ID"
        GET_STATUS=$(curl -s $SCAN_STATUS 2>&1)
        echo $GET_STATUS | jq
        SCAN_TOTAL=$(curl -s $SCAN_STATUS 2>&1 |  jq .status | sed 's/"//g')
        echo $SCAN_TOTAL
        # echo $STATUS_DISPLAY | jq
        # SCAN_STATUS=$(curl -s $SCAN_STATUS 2>&1 |  jq .status | sed 's/"//g')
        sleep 1
        echo -e '\0033\0143'
    done
}



PROXY_HOST=$1
PROXY_PORT=$2
HOST=$3
TARGET=$(curl $PROXY_HOST 2>&1 -s -v | grep Location | awk {'print $3'})


ensure_host_up 