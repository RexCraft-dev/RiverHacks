@echo off
cd /d "%~dp0"
python -m venv venv
call venv\\Scripts\\activate
python scores.py --file scores.csv --overall --export overall_scores.txt
python scores.py --file scores.csv --list --exportall
python scores.py --file scores.csv --cheat --export cheat_check.txt

pause