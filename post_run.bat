@echo off
python scores.py --file sample_scores.csv --overall --export overall_scores.txt
python scores.py --file sample_scores.csv --list --exportall
python scores.py --file sample_scores.csv --cheat --export cheat_check.txt

pause