
# RiverHacks2025 – Judging and Project Tools

This repository contains the judging system, project processing tools, and Airtable integration scripts for RiverHacks2025. It supports CSV-based scoring, participant contact extraction, and automated result exports for each track.

## Project Structure

```
RiverHacks/
├── data/                  # Contains scores.csv, projects.csv, judges.txt
├── output/                # Generated outputs (rankings, contacts, assignments)
├── .env                   # Airtable API keys and table config (not tracked in Git)
├── dependencies.bat       # Set up Python virtual environment (Windows)
├── run_fetch.bat          # Fetch Airtable data to CSVs (Windows)
├── run_scores.bat         # Run scoring/export script (Windows)
├── dependencies.sh        # Equivalent setup for Linux/macOS
├── run_fetch.sh           # Equivalent fetch script for Linux/macOS
├── run_scores.sh          # Equivalent scoring script for Linux/macOS
├── fetch_tables.py        # Downloads ProjectTable and JudgingTable from Airtable
├── projects.py            # Handles project listing, contact extraction, judge assignment
├── scores.py              # Processes score data, exports rankings and track results
└── requirements.txt       # Minimal dependencies list
```

## Setup Instructions

### 1. Install Requirements (Virtual Environment Recommended)

**Windows:**

```cmd
dependencies.bat
```

**Linux/macOS:**

```bash
./dependencies.sh
```

This creates and activates a virtual environment and installs dependencies from `requirements.txt`.

### 2. Configure Environment

Create a `.env` file in the root directory with the following:

```
API_ID=your_airtable_base_id
API_KEY=your_airtable_api_key
PROJECT_TABLE=ProjectTable
JUDGING_TABLE=JudgingTable
```

### 3. Fetch Airtable Data

**Windows:**

```cmd
run_fetch.bat
```

**Linux/macOS:**

```bash
./run_fetch.sh
```

This will fetch data from Airtable and save it to:

- `data/projects.csv`
- `data/scores.csv`

### 4. Process Scores and Export Results

**Windows:**

```cmd
run_scores.bat
```

**Linux/macOS:**

```bash
./run_scores.sh
```

This will generate track-specific rankings and overall results in the `output/` directory.

## Command-Line Arguments Reference

### `projects.py` Options

| Argument      | Description                                                        |
|---------------|--------------------------------------------------------------------|
| `--file`      | Path to the `projects.csv` file                                    |
| `--projects`  | Lists all submitted project names                                  |
| `--contacts`  | Extracts contact information for a specific project or all (`"."`) |
| `--export`    | Export contacts to a file (used with `--contacts`)                 |
| `--assign`    | Assigns judges to projects (minimum 3 per team, balanced)          |

### `scores.py` Options

| Argument       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `--file`       | Path to the `scores.csv` file                                               |
| `--overall`    | Display overall ranked results                                              |
| `--count`      | Limit output to top N results                                               |
| `--track`      | Filter and display results for a specific track (1–7)                       |
| `--cheat`      | Show all projects flagged as cheating                                       |
| `--export`     | Export results to a specific file (used with `--overall`, `--track`, or `--cheat`) |
| `--exportall`  | Export rankings for each track and overall to the `output/` folder          |
| `--list`       | Print combined results by track                                             |

## Command Examples

**View contacts from a specific project or all projects:**

```bash
python projects.py --file projects.csv --contacts "Project Name" --export .
```

**List all projects:**

```bash
python projects.py --file projects.csv --projects
```

**Assign judges to projects:**

```bash
python projects.py --file projects.csv --assign
```

**Export a combined list of track results:**

```bash
python scores.py --file scores.csv --list --export all
```
