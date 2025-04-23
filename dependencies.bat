@echo off
cd /d "%~dp0"
python -m venv venv
call venv\\Scripts\\activate

echo "Checking dependencies"
pip install -r requirements.txt

pause