# Hackathon Score Processor

This script processes and exports hackathon project scores from a CSV file. It supports overall and track-based rankings, suspected cheating detection, and various export formats.

## Features

- Computes average project scores across four judging categories
- Filters and ranks projects within specific judging tracks
- Flags projects marked with suspected cheating
- Outputs to separate `.txt` files by track or combined list
- Supports CLI for filtering, ranking, and exporting

## Judging Categories

- Innovation
- Value & Impact
- Completeness
- Technical Implementation

## Judging Tracks

- Best Overall
- Best Design
- Cybersecurity
- webAI
- Community Engagement
- Community Choice

## Requirements

- Python 3.7+
- pandas

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Required
```bash
python script.py --file input.csv
```
(Note: The CSV file must be placed in the `data/` directory.)

### Options
- `--overall` : Print ranked list of all projects
- `--track [index]` : Show ranked list for a track (1–6)
- `--cheat` : List all flagged projects for cheating
- `--count [N]` : Limit result output to top N
- `--export [filename.csv]` : Export the last result to CSV
- `--exportall` : Export overall + track results to individual files in `output/`
- `--tolist` : Export all results (overall + tracks) to one file: `output/list_results.txt`

### Example Commands

Top 10 overall projects:
```bash
python script.py --file scores.csv --overall --count 10
```

Export everything to separate `.txt` files:
```bash
python script.py --file scores.csv --exportall
```

Export a single merged list:
```bash
python script.py --file scores.csv --tolist
```

Display cybersecurity results:
```bash
python script.py --file scores.csv --track 3
```

## Output Behavior
- Rankings are sorted from highest to lowest
- Ranks begin at 1 for each list
- Files are written to the `/output` folder

## License

MIT License
