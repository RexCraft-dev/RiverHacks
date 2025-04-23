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
echo DEMO_ID=appCmzIf1WO7chBNq
echo DEMO_KEY=patEcZHawTWU6L3Jv.18784485a86ac74144cc18eaba7b1bc5e2c107b6b051a4f2a09cfcb9039872bb
echo PROJECT_TABLE=ProjectTable
echo JUDGING_TABLE=JudgingTable
echo JUDGES_TABLE=Judges
) > .env

echo [-] .env file created successfully...
pause
