PORT=1337
zap.sh -daemon -host $(hostname -I) -port 8080  \
-config api.addrs.addr.name='.*' \
-config api.addrs.addr.regex=true \
-config api.disablekey=true &