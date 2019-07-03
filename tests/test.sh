curl -X POST $FLASK/api/v1/spider/start \ 
    --header "Content-Type: application/json" \
    --data '{"url": "https://example.com"}'