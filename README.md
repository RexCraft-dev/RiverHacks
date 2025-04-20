# Hackathon Score Processor

This script helps automate the scoring, ranking, and exporting of hackathon project evaluations based on CSV data. It supports calculating average scores across categories, viewing and exporting track-specific rankings, flagging potential cheaters, and producing formatted output in both CSV and plain text formats.

## Features

- Calculates average project scores across multiple judging categories
- Supports filtering and exporting by individual judging tracks
- Flags entries marked for suspected cheating
- Exports ranked results in both individual and combined formats
- CLI-based control for filtering, limiting, and formatting outputs

## Judging Categories

- Innovation
- Value & Impact
- Completeness
- Technical Implementation

## Available Tracks

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
python script.py --file path/to/data.csv
```

### Optional Flags

- `--overall` - Print overall project rankings to the console
- `--track [index]` - Show results for a specific track (use index from 1-5)
- `--cheat` - Show projects marked with suspected cheating
- `--count [N]` - Show only the top N projects in any output
- `--export [filename.csv]` - Export the most recent results to a CSV
- `--exportall` - Export overall and track rankings into separate `.txt` files
- `--inline` - Export overall and all track results into one combined `.txt` file

### Example Commands

View top 5 projects overall:
```bash
python script.py --file results.csv --overall --count 5
```

Export each track and overall results to separate text files:
```bash
python script.py --file results.csv --exportall --count 10
```

Export all rankings (top 10) to a single file:
```bash
python script.py --file results.csv --inline --count 10
```

Show only projects suspected of cheating:
```bash
python script.py --file results.csv --cheat
```

## Output
- Rankings are sorted highest to lowest by overall average score
- Rank numbers begin at 1 for each section
- Results can be printed to console, saved per category, or saved inline to a single file

## License

MIT License
