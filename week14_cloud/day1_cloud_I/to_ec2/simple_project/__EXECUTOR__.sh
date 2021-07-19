#!/bin/bash
# Author: Gabriel Vázquez Torres @gabvaztor
# Another way:

# https://discuss.streamlit.io/t/problem-deploying-streamlit-app-with-docker/1644/4

DOCKER_BUILD="ml_project_image:latest"
DOCKER_ID=$(docker ps -a -q --filter ancestor=${DOCKER_BUILD} --format="{{.ID}}")
sudo docker rm $(docker stop $(docker ps -a -q --filter ancestor=${DOCKER_BUILD} --format="{{.ID}}"))

sudo docker kill ${DOCKER_BUILD}
sudo docker rmi -f ${DOCKER_BUILD}
sudo docker rm -v -f ${DOCKER_BUILD}
sudo docker rmi $(docker images | grep ${DOCKER_BUILD})
sudo docker kill ${DOCKER_ID}
sudo docker rmi -f ${DOCKER_ID}
sudo docker rm -v -f ${DOCKER_ID}
sudo docker rmi $(docker images | grep ${DOCKER_ID})

sudo docker build -t ${DOCKER_BUILD} .
sudo docker run -td -p 6060:6060 -p 8501:8501 ${DOCKER_BUILD}

DOCKER_ID=$(docker ps -a -q --filter ancestor=${DOCKER_BUILD} --format="{{.ID}}")

sudo docker exec ${DOCKER_ID} sh -c "echo The local IP is:"
sudo docker exec ${DOCKER_ID} sh -c "hostname -I"

#sudo docker exec ${DOCKER_ID} sh -c "python3 ./src/api/server.py"
sudo docker exec ${DOCKER_ID} sh -c "nohup python3 ./src/api/server.py > server.log &"

#sudo docker exec ${DOCKER_ID} sh -c "streamlit run ./src/dashboard/app.py"
#sudo docker exec ${DOCKER_ID} sh -c "nohup streamlit run ./src/dashboard/app.py > app.log &"

# sudo docker exec ml_project_image:latest sh -c "streamlit run ./src/dashboard/app.py"
#sudo docker exec ${DOCKER_BUILD} sh -c "streamlit run ./src/dashboard/app.py"
