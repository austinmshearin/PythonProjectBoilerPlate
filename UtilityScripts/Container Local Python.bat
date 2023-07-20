@ECHO OFF
cd /d %~dp0
cd ..
ECHO Building image and deploying container
docker build -t localpython:localpython -f ./Docker/Python .
docker run -d --name LocalPython -v "%cd%/LocalPythonContainerVolume":"/home/volume" localpython:localpython
ECHO Press enter to close the docker image
pause
ECHO Stopping container and deleting container and image
docker stop LocalPython
docker rm LocalPython
docker image rm localpython:localpython
ECHO Container stopped and container and image deleted
ECHO Press enter to close window
pause