@echo off
cd /d %~dp0
cd ..
for %%I in (.) do set CurrDirName=%%~nxI
set VirEnvName=%CurrDirName%_VirEnv
call "./%VirEnvName%/Scripts/activate.bat"
pdoc -p 8090 ./package
cmd /k