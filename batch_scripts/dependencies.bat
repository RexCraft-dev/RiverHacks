@echo off
cd ..
python -m venv venv
call venv\\Scripts\\activate

echo "Checking dependencies"
pip install -r requirements.txt

echo "Creating directories"
python fetch_tables.py --dir

pause