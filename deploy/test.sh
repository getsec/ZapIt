

curl -X POST localhost:5000/api/v1/spider/start -d '{"url":"https://wawanesa.com"}' -H "Content-Type: application/json" | jq

curl -X POST localhost:5000/api/v1/spider/results -d '{"scan_id":"0"}' -H "Content-Type: application/json" | jq

curl -X POST localhost:5000/api/v1/results/summary -d '{"url":"https://wawanesa.com"}' -H "Content-Type: application/json" | jq


curl -X POST localhost:5000/api/v1/results/full -H "Content-Type: application/json" | jq