# Hackathon Score Processor

This tool helps automate the parsing, scoring, and exporting of hackathon project evaluations from CSV files. It calculates overall scores, evaluates track-specific rankings, identifies potential cheaters, and supports exporting formatted results to CSV or text files.

## Features

- Calculates average scores across judging categories
- Ranks projects by overall and track-specific performance
- Flags projects marked for potential cheating
- CLI-friendly: supports quick filtering, exporting, and display
- Outputs results to CSV or plain text for distribution

## Judging Criteria Handled

- Innovation  
- Value & Impact  
- Completeness  
- Technical Implementation  

## Supported Tracks

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

### Basic Example
```bash
python script.py --file results.csv --overall
```

### View Results by Track
```bash
python script.py --file results.csv --track 2
```

### Show Suspected Cheating Projects
```bash
python script.py --file results.csv --cheat
```

### Export Overall and Track Rankings to Files
```bash
python script.py --file results.csv --all --export output/results
```

### Export a Single View to CSV
```bash
python script.py --file results.csv --overall --export overall.csv
```

## Notes

- Column names in the CSV must match the expected format. If using another form, adjust the column renaming logic in `load_data()`.
- Rankings are sorted with one entry per project.
- `--all` will export all processed results to individual `.txt` files for each track and overall rankings.

## License

MIT License

