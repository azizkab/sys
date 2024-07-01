# liste des commandes pour créer un environnement virtuel en Python

mkdir hexagone-b2-tps
cd hexagone-b2-tps
clear
python -m venv bibenv
ls -l
source ./bibenv/bin/activate
pip list
pip install requests
pip list
clear
pip freeze
pip freeze > requirements.txt
cat requirements.txt
python -m venv bibenv2
source ./bibenv2/bin/activate
pip list
cat requirements.txt
pip install -r requirements.txt
pip list

git init
git config --global init.defaultBranch main

# create the image
docker build -t bib:latest .

# create a container and map the local save.json with container version
docker run -it --rm -v ./save.json:/app/save.json  bib:latest python /app/bib.py

# create client image
docker build -t bibclient:latest -f Dockerfile-client .

# create server image
docker build -t bibserver:latest -f Dockerfile-server .

# run client container
docker run -it -e BIB_PORT=8888 -e BIB_HOST=172.17.0.2 bibclient:latest

# run client container with custom python client script
docker run -it -e BIB_PORT=8888 -e BIB_HOST=172.17.0.2 -v ./client.py:/app/client.py bibclient:latest

# run server container
docker run -p 9999:8888 -e BIB_PORT=8888 -e BIB_HOST=0.0.0.0 -v ./save.json:/app/save.json  bibserver:latest

# run prometheus
docker run -d -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml -p 9090:9090 prom/prometheus

# run custom exporter postgresql
docker run -e DATA_SOURCE_NAME="postgresql://postgres:password@172.17.0.2:5432/human_bot_db?sslmode=disable" quay.io/prometheuscommunity/postgres-exporter
