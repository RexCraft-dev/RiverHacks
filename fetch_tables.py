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
BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY")
PROJECT_TABLE = os.getenv("PROJECT_TABLE")
JUDGING_TABLE = os.getenv("JUDGING_TABLE")
JUDGES_TABLE = os.getenv("JUDGES_TABLE")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}


def ensure_directories():
    print("[!] Checking for directories...")
    dirs = [
        "data",
        "output",
        "output/projects",
        "output/judging"
    ]
    for path in dirs:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"[+] Created directory: {path}")


def ping_airtable():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{PROJECT_TABLE}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            print("[+] Airtable base is reachable Status Code: 200).")
        else:
            print(f"[!] Received status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error pinging Airtable: {e}")


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

        records.extend([{"id": rec["id"], **rec["fields"]} for rec in data.get("records", [])])

        offset = data.get("offset")
        if not offset:
            break

    return pd.DataFrame(records)


def patch_airtable_field(table_name, record_id, field_name, new_value):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}/{record_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            field_name: new_value
        }
    }

    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def get_record_id_by_project_name(project_name):
    df = fetch_airtable_table(PROJECT_TABLE)
    match = df[df["Project Name"] == project_name]
    if not match.empty:
        return match.iloc[0]["id"]
    return None


def main():
    parser = argparse.ArgumentParser(description="Process hackathon scores.")
    parser.add_argument("--projects", action="store_true", help="Path to CSV file")
    parser.add_argument("--scores", action="store_true", help="Export results to a CSV file")
    parser.add_argument("--judges", action="store_true", help="Show list of participant's contact info")
    parser.add_argument("--ping", action="store_true", help="Ping Airtable base for connectivity check")

    args = parser.parse_args()

    ensure_directories()

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
        judging_df = judging_df["Name"]
        print(judging_df)
        judging_df.to_csv("data/judges.txt", sep="\n", index=False, header=False)
        print("[-] Saved as judges.txt successfully...")

    if args.ping:
        ping_airtable()


if __name__ == "__main__":
    main()
