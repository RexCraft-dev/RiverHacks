import os
import pandas as pd
import argparse
from itertools import combinations
from collections import defaultdict
from fetch_tables import (get_record_id_by_project_name,
                          patch_airtable_field,
                          PROJECT_TABLE)


def save_txt_and_csv(txt_content, df=None, base_path="output", filename="output"):
    os.makedirs(base_path, exist_ok=True)

    txt_path = os.path.join(base_path, f"{filename}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(txt_content)

    if df is not None and isinstance(df, pd.DataFrame):
        csv_path = os.path.join(base_path, f"{filename}.csv")
        df.to_csv(csv_path, index=False)


def list_projects(df):
    df = df[["Project Name"]].copy()
    df.index += 1
    df.index.name = "Table"

    lines = ["RIVERHACKS25 PROJECT SUBMISSIONS",
             "-------------------------------------------------",
             "Table   Project"]

    for idx, row in df.iterrows():
        lines.append(f"{idx:<8}{row['Project Name']}")

    return "\n".join(lines), df


def extract_contacts(df, project="."):
    df = df.rename(columns={"Project Name": "ProjectName"})

    contact_columns = [
        ("ProjectName", "Member 1 Name", "Member 1 Email"),
        ("ProjectName", "Member 2 Name", "Member 2 Email"),
        ("ProjectName", "Member 3 Name", "Member 3 Email"),
        ("ProjectName", "Member 4 Name", "Member 4 Email"),
        ("ProjectName", "Member 5 Name", "Member 5 Email")
    ]

    output_lines = []
    contacts = []

    if project.lower() == ".":
        projects = df["ProjectName"].unique()
    else:
        if project not in df["ProjectName"].values:
            print(f"[!] Project '{project}' not found.")
            return "", pd.DataFrame()
        projects = [project]

    df = df.fillna("")

    for proj in projects:
        output_lines.append(proj)
        output_lines.append("-" * 45)

        row = df[df["ProjectName"] == proj].iloc[0]

        for proj_col, name_col, email_col in contact_columns:
            project = str(row.get(proj_col, "")).strip()
            name = str(row.get(name_col, "")).strip()
            email = str(row.get(email_col, "")).strip()
            if name or email or project:
                output_lines.append(f"{name:<20} {email:<20} {project:<25}")
                contacts.append({"Name": name, "Email": email, "Project": project})

        output_lines.append("")

    return "\n".join(output_lines), pd.DataFrame(contacts)


def assign_tables(projects_df, count=3):
    print("[*] Loading project files...")

    with open("data/judges.txt", "r") as f:
        judges = [line.strip() for line in f.readlines() if line.strip()]

    project_names = projects_df["Project Name"].tolist()
    k = count

    judge_counts = defaultdict(int)
    assignments = []
    used_combos = set()
    judge_tabs = {}

    def get_balanced_combo(judges, judge_counts, used_combos, k):
        sorted_judges = sorted(judges, key=lambda j: judge_counts[j])
        combos = combinations(sorted_judges, k)
        for combo in combos:
            if tuple(sorted(combo)) not in used_combos:
                return combo
        return None

    for i, project in enumerate(project_names, start=1):
        combo = get_balanced_combo(judges, judge_counts, used_combos, k=k)
        if combo:
            used_combos.add(tuple(sorted(combo)))
            for judge in combo:
                assignments.append({
                    "Table Number": i,
                    "Project Name": project,
                    "Judge Name": judge
                })
                judge_counts[judge] += 1

            record_id = get_record_id_by_project_name(project)
            if record_id:
                try:
                    patch_airtable_field(PROJECT_TABLE, record_id, "Table", i)
                    print(f"[+] [TABLE {i:<2}]".ljust(10) + f" {project.ljust(20)}")
                except Exception as e:
                    print(f"[!] Failed to update '{project}' in Airtable: {e}")

    assignment_df = pd.DataFrame(assignments)
    grouped = assignment_df.groupby("Judge Name")

    formatted_output = []
    for judge, group in grouped:
        formatted_output.append(judge)
        formatted_output.append("--------------------------------")
        formatted_output.append("Table      Project")
        for _, row in group.iterrows():
            formatted_output.append(f"{row['Table Number']:<10} {row['Project Name']}")
        formatted_output.append("")

        judge_tabs[judge] = group[["Table Number", "Project Name"]].sort_values("Table Number")

    output = "\n".join(formatted_output)
    save_txt_and_csv(output, assignment_df, base_path="output/judging", filename="judge_assignments")

    with pd.ExcelWriter("output/judging/judge_assignments.xlsx") as writer:
        for judge, df in judge_tabs.items():
            df["Judge"] = judge
            df = df.rename(columns={"Table Number": "Table", "Project Name": "Project"})
            df = df[["Judge", "Table", "Project"]]
            clean_name = judge[:31].replace("/", "_").replace("\\", "_")
            df.to_excel(writer, sheet_name=clean_name, index=False)

    print(f"[-] Judges assigned to projects successfully...")
    return output


def main():
    parser = argparse.ArgumentParser(description="Process hackathon scores.")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--export", help="Export results to a CSV file")
    parser.add_argument("--contacts", help="Show list of participant's contact info")
    parser.add_argument("--projects", action="store_true", help="Show list of all projects")
    parser.add_argument("--assign", action="store_true", help="Assigns judges to projects for scoring")

    args = parser.parse_args()
    file_path = f"data/{args.file}"

    if args.assign:
        print("[*] Parsing project data...")
        df = pd.read_csv(file_path)
        result_text = assign_tables(df)

    if args.contacts:
        df = pd.read_csv(file_path)
        print("[*] Parsing contact information...")
        text, contact_df = extract_contacts(df, args.contacts)
        save_txt_and_csv(text, contact_df, base_path="output/projects", filename=f"contacts_{args.export or 'list'}")

    if args.projects:
        print("[*] Loading project data...")
        df = pd.read_csv(file_path)
        projects_text, project_df = list_projects(df)
        save_txt_and_csv(projects_text, project_df, base_path="output/projects", filename="projects_list")


if __name__ == "__main__":
    main()
