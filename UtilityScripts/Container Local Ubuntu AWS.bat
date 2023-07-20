@ECHO OFF
cd /d %~dp0
cd ..
ECHO Building image and deploying container
for /f %%i in ('aws --profile default configure get aws_access_key_id') do set AWS_ACCESS_KEY_ID=%%i
for /f %%i in ('aws --profile default configure get aws_secret_access_key') do set AWS_SECRET_ACCESS_KEY=%%i
docker build -t localubuntuaws:localubuntuaws -f ./Docker/UbuntuAWS .
docker run -d -e AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%  -e AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY% --name LocalUbuntuAWS -v "%cd%/LocalUbuntuAWSContainerVolume":"/home/volume" localubuntuaws:localubuntuaws
ECHO Press enter to close the docker image
pause
ECHO Stopping container and deleting container and image
docker stop LocalUbuntuAWS
docker rm LocalUbuntuAWS
docker image rm localubuntuaws:localubuntuaws
ECHO Container stopped and container and image deleted
ECHO Press enter to close window
pause
