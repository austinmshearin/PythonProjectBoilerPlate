@ECHO OFF
cd /d %~dp0
cd ..
for %%I in (.) do set CurrDirName=%%~nxI
set VirEnvName=%CurrDirName%_VirEnv
CALL ./%VirEnvName%/Scripts/activate.bat
python -m pip freeze > delete.txt
python -m pip uninstall -r delete.txt -y
del delete.txt
pause
