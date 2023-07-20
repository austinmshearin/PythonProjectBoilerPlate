@ECHO OFF
ECHO Deploying MySQL database container
docker run --name db -v "%cd%/../DB/MySQLContainerVolume":"/var/lib/mysql" -e MYSQL_ROOT_PASSWORD="root" -p 3306:3306 -d mysql:8
ECHO Press enter to close the database container
pause
ECHO Stopping and deleting container
docker stop db
docker rm db
ECHO Container stopped and deleted
ECHO Press enter to close window
pause
