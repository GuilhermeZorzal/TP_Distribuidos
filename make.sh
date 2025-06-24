cleanup() {
  echo "Encerrando todos os processos..."
  kill $server $serverName $client
}
trap cleanup EXIT

pyro5-ns --host 0.0.0.0 &
serverName=$!

cd ./server-app/ && python ./server.py --local &
server=$!

sleep 5

cd ./frontend/ && python ./interface.py --local &
client=$!

wait $client
