@echo off

python scores.py --file sample_scores.csv --overall --export overall_scores.txt

python scores.py --file sample_scores.csv --list --export all

python scores.py --file sample_scores.csv --cheat --export cheat_check.txt

python projects.py --file sample_projects.csv --projects

python projects.py --file sample_projects.csv --assign

pause