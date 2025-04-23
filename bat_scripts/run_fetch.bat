@echo off
cd ..
call venv\\Scripts\\activate

echo [SCRIPT] Fetching table data...
python fetch_tables.py --projects --judges

echo [SCRIPT] Extracting projects...
python projects.py --file projects.csv --projects

echo [SCRIPT] Assigning judges to projects...
python projects.py --file projects.csv --assign

echo [SCRIPT] Extracting contacts list...
python projects.py --file projects.csv --contacts . --export .

echo [SCRIPT] All processes completed successfully...

pause