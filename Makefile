all: 
	sh make.sh

install: 
	pip install -r requirements.txt

client: 
	cd frontend && python ./interface.py --local

server: 
	cd server-app && python ./server.py --local

name-server:
	pyro5-ns --host 0.0.0.0

