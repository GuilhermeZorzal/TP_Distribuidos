install: 
	pip install -r requirements.txt

client: 
	python ./frontend/interface.py

server: 
	python ./server-app/server.py
