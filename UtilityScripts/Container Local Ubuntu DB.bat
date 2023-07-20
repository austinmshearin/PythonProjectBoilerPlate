@ECHO OFF
cd /d %~dp0
cd ..
ECHO Building image and deploying container
docker network create local_network
docker network connect local_network db
docker build -t localubuntudb:localubuntudb -f ./Docker/UbuntuDB .
docker run -d --name LocalUbuntuDB -v "%cd%/LocalUbuntuDBContainerVolume":"/home/volume" --net local_network localubuntudb:localubuntudb
ECHO press enter to close development docker image
pause
ECHO Stopping container and deleting container and image
docker stop LocalUbuntuDB
docker rm LocalUbuntuDB
docker image rm localubuntudb:localubuntudb
docker network disconnect local_network db
docker network rm local_network
ECHO Container stopped and container and image deleted
ECHO Press enter to close window
pause