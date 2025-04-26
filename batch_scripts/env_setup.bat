@echo off
setlocal

:: Prompt user for input
set /p BASE_ID=Enter your Base ID:
set /p API_KEY=Enter your API Key:

cd ..

:: Create or overwrite .env file with the values
(
echo BASE_ID=%BASE_ID%
echo API_KEY=%API_KEY%
echo PROJECT_TABLE=ProjectTable
echo JUDGING_TABLE=JudgingTable
echo JUDGES_TABLE=Judges
) > .env

python fetch_tables.py --ping

echo [-] .env file created successfully...
pause
