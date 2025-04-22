# RiverHacks Score Parser

This Python script processes project scores and team contact data from CSV exports used in hackathons like RiverHacks. It supports category-based scoring, track-based filtering, data exports, and email contact listings.

## Features

- Parse and compute average scores from multiple judges
- Filter by track or overall category
- Print or export results to individual or combined files
- List flagged "cheating" projects
- Generate contact rosters for all or individual projects

---

## Setup

### Requirements
- Python 3.7+
- pandas

Install with:
```bash
pip install -r requirements.txt
```

### File Structure
```
project-root/
├── data/
│   └── your_input_file.csv
├── output/
│   ├── best_overall.txt
│   ├── cybersecurity.txt
│   └── contacts_all.txt
└── script.py
```

CSV input files must be placed in the `data/` folder. All results are written to the `output/` folder.

---

## Usage

### Required
```bash
python scores.py --file yourfile.csv
```

### Options
- `--overall` : Show top overall projects
- `--track [index]` : Show results for a specific track (1–5)
- `--count [N]` : Show only the top N results
- `--cheat` : Show all projects flagged for cheating
- `--export [filename.csv]` : Export last viewed results to CSV
- `--exportall` : Export all rankings (overall + tracks) to individual files
- `--tolist` : Export all rankings to a single text file
- `--contacts [project|all]` : Generate contact list for one or all projects

### Example Commands

Top 10 overall projects:
```bash
python scores.py --file projects_uneven.csv --overall --count 10
```

Export all rankings to files in `/output`:
```bash
python scores.py --file projects_uneven.csv --exportall
```

Export all results to a single file:
```bash
python scores.py --file projects_uneven.csv --tolist
```

Show contacts for one project:
```bash
python scores.py --file projects_uneven.csv --contacts "Project XYZ"
```

Show all contacts:
```bash
python scores.py --file projects_uneven.csv --contacts all
```

---

## Tracks (by index)
1. Best Overall
2. Best Design
3. Cybersecurity
4. webAI
5. Community Engagement
6. Community Choice

---

## Outputs

- All ranked results are written to `.txt` files in `output/`
- Rankings start at 1 and are sorted by average score descending
- Contact files include project name and a table of team names/emails

---

## License

MIT License

