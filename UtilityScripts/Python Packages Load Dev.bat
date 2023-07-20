@ECHO OFF
cd /d %~dp0
cd ..
for %%I in (.) do set CurrDirName=%%~nxI
set VirEnvName=%CurrDirName%_VirEnv
CALL ./%VirEnvName%/Scripts/activate.bat
python -m pip install -r dev_requirements.txt
pause
