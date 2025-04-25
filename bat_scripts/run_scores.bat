@echo off
cd ..
call venv\\Scripts\\activate

python fetch_tables.py --ping

echo [SCRIPT] Updating table data...
python fetch_tables.py --scores

echo [SCRIPT] Extracting overall team scores...
python scores.py --file scores.csv --overall --export overall_scores.txt

echo [SCRIPT] Extracting all track scores...
python scores.py --file scores.csv --exportall

echo [SCRIPT] Extracting all track scores...
python scores.py --file scores.csv --list all --export all

echo [SCRIPT] Checking for potential cheating teams...
python scores.py --file scores.csv --cheat --export cheat_check.txt

echo [SCRIPT] All processes completed successfully...
pause