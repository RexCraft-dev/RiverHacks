import os
import requests
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import argparse

# Load .env relative to the script location
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path)

# Airtable config (demo credentials)
BASE_ID = os.getenv("DEMO_ID")
API_KEY = os.getenv("DEMO_KEY")
PROJECT_TABLE = os.getenv("PROJECT_TABLE")
JUDGING_TABLE = os.getenv("JUDGING_TABLE")
JUDGES_TABLE = os.getenv("JUDGES_TABLE")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}


def fetch_airtable_table(table_name):
    records = []
    offset = None
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"

    while True:
        params = {}
        if offset:
            params["offset"] = offset

        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        records.extend(data.get("records", []))
        offset = data.get("offset")

        if not offset:
            break

    return pd.DataFrame([rec["fields"] for rec in records])


def main():
    parser = argparse.ArgumentParser(description="Process hackathon scores.")
    parser.add_argument("--projects", action="store_true", help="Path to CSV file")
    parser.add_argument("--scores", action="store_true", help="Export results to a CSV file")
    parser.add_argument("--judges", action="store_true", help="Show list of participant's contact info")

    args = parser.parse_args()

    if args.projects:
        print("[*] Fetching ProjectTable from Airtable...")
        projects_df = fetch_airtable_table(PROJECT_TABLE)
        projects_df.to_csv("data/projects.csv", index=False)
        print("[-] Saved as projects.csv successfully...")

    if args.scores:
        print("[*] Fetching JudgingTable from Airtable...")
        judging_df = fetch_airtable_table(JUDGING_TABLE)
        judging_df.to_csv("data/scores.csv", index=False)
        print("[-] Saved as scores.csv successfully...")

    if args.judges:
        print("[*] Fetching Judges from Airtable...")
        judging_df = fetch_airtable_table(JUDGES_TABLE)
        judging_df.to_csv("data/judges.txt", sep="\n", index=False, header=False)
        print("[-] Saved as judges.txt successfully...")


if __name__ == "__main__":
    main()
