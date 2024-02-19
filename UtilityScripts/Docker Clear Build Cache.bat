@echo off
echo All cached objects not associated with tagged images will be cleared
set /p dummy=Press enter to clear cached objects or close to cancel
echo Clearing cached objects
docker builder prune
echo Cached objects cleared
set /p dummy=Press enter to exit
