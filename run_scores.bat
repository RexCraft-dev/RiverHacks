@echo off
cd /d "%~dp0"
call venv\\Scripts\\activate

echo [SCRIPT] Updating table data...
python fetch_tables.py

echo [SCRIPT] Extracting overall team scores...
python scores.py --file scores.csv --overall --export overall_scores.txt

echo [SCRIPT] Extracting all track scores...
python scores.py --file scores.csv --exportall

echo [SCRIPT] Extracting all track scores...
python scores.py --file scores.csv --list --export all

echo [SCRIPT] Checking for potential cheating teams...
python scores.py --file scores.csv --cheat --export cheat_check.txt

echo [SCRIPT] All processes completed successfully...
pause