# web_App_Depolyment_AWS_Using_Docker
conda create -n imageclass python=3.11 -y 

conda activate imageclass

1. Login with your AWS console and launch an EC2 instance
2. Run the following commands
Note: Do the port mapping to this port:- 8080

sudo apt-get update -y

sudo apt-get upgrade

#Install Docker

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
git clone "your-project"
docker build -t entbappy/imageclswebapp:latest . 
docker images -a  
docker run -d -p 8080:8080 entbappy/imageclswebapp 
docker ps  
docker stop container_id
docker rm $(docker ps -a -q)
docker login 
docker push entbappy/imageclswebapp:latest 
docker rmi entbappy/imageclswebapp:latest
docker pull entbappy/imageclswebapp