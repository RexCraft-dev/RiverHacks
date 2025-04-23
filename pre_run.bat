@echo off

python projects.py --file sample_projects.csv --projects
python projects.py --file sample_projects.csv --assign
python projects.py --file sample_projects.csv --contacts . --export .

pause