@ECHO OFF
cd /d %~dp0
cd ..
ECHO Building image and deploying container
docker build -t localubuntu:localubuntu -f ./Docker/Ubuntu .
docker run -d --name LocalUbuntu -v "%cd%/LocalUbuntuContainerVolume":"/home/volume" localubuntu:localubuntu
ECHO Press enter to close the docker image
pause
ECHO Stopping container and deleting container and image
docker stop LocalUbuntu
docker rm LocalUbuntu
docker image rm localubuntu:localubuntu
ECHO Container stopped and container and image deleted
ECHO Press enter to close window
pause
