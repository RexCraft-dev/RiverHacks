Great! Since there's a `requirements.txt` file, here's the revised `README.md` with the proper setup instructions and a cleaner structure:

---

# RiverHacks25 Judging System

This repository contains scripts to manage project data, assign judges, and analyze hackathon scoring for **RiverHacks25**.

---

## Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## File Structure

```
data/
├── projects.csv         # Project submissions
├── judges.txt           # List of judges (one per line)
├── judging.csv          # Judging results (one row per judge per project)

output/
├── *.txt                # Generated judging results and contact exports

projects.py              # For assigning judges and viewing project/contact info
scores.py                # For scoring, rankings, and exporting results
requirements.txt         # Python dependencies
```

---

## Commands

### List All Submitted Projects

```bash
python projects.py --file projects.csv --projects
```

---

### Extract Contact Info

```bash
# Single project
python projects.py --file projects.csv --contacts "Project 1"

# All projects
python projects.py --file projects.csv --contacts "." --export list
```

---

### Assign Judges to Teams (Balanced, Non-Repeating)

```bash
python projects.py --file projects.csv --assign
```

Outputs a formatted judge table list to `output/judge_assignments.txt`.

---

## Scoring and Results

### Overall Rankings

```bash
python scores.py --file judging.csv --overall
```

---

### Track Rankings

```bash
python scores.py --file judging.csv --track 4 --count 5
```

Track Index Reference:
```
1 - Main Track
2 - Disaster Response
3 - Accessible City
4 - Cybersecurity
5 - webAI
6 - Mobility Access
7 - Public Safety Insights
```

---

### Export All Rankings (One File Per Track)

```bash
python scores.py --file judging.csv --exportall
```

---

### Export Summary of All Track Results (Single File)

```bash
python scores.py --file judging.csv --list --export
```

---

### View Suspected Cheating Submissions

```bash
python scores.py --file judging.csv --cheat
```

---

## Notes

- If your CSV columns differ, adjust the renaming section in `load_data()` in `scores.py`.
- All output files will be written to the `output/` directory.
