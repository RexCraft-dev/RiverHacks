@echo off
cd /d "%~dp0"
python -m venv venv
call venv\\Scripts\\activate
echo "Fetching table data..."
python fetch_tables.py
python projects.py --file projects.csv --projects
python projects.py --file projects.csv --assign
python projects.py --file projects.csv --contacts . --export .
pause