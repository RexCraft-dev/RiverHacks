import pandas as pd
import argparse
import re
import random
from itertools import combinations
from collections import defaultdict


def list_projects(df):
    projects = []
    df = df.rename(columns={"Project Name": "ProjectName"})
    df = df["ProjectName"].values
    df_string = "\n".join(df)
    projects.append("RIVERHACKS25 PROJECT SUBMISSIONS\n" +
                    "-------------------------------------------------\n" +
                    df_string)
    projects = "\n".join(projects)
    return projects


def extract_contacts(df, project="."):
    df = df.rename(columns={"Project Name": "ProjectName"})

    # Define the relevant columns for names and emails
    contact_columns = [
        ("Member 1 Name", "Member 1 Email"),
        ("Member 2 Name", "Member 2 Email"),
        ("Member 3 Name", "Member 3 Email"),
        ("Member 4 Name", "Member 4 Email"),
        ("Member 5 Name", "Member 5 Email")
    ]

    output_lines = []

    # Determine which projects to process
    if project.lower() == ".":
        projects = df["ProjectName"].unique()
    else:
        if project not in df["ProjectName"].values:
            print(f"[!] Project '{project}' not found.")
            return
        projects = [project]

    for proj in projects:
        output_lines.append(proj)
        output_lines.append("-" * 45)

        row = df[df["ProjectName"] == proj].iloc[0]

        for name_col, email_col in contact_columns:
            name = str(row.get(name_col, "")).strip()
            email = str(row.get(email_col, "")).strip()
            if name or email:
                output_lines.append(f"{name:<20} {email}")

        output_lines.append("")  # Add space between projects

    full_output = "\n".join(output_lines)

    return full_output


def assign_tables(projects_df, count=3):
    print("[-] Loading project files...")

    # Load data
    with open("data/judges.txt", "r") as f:
        judges = [line.strip() for line in f.readlines() if line.strip()]

    project_names = projects_df["Project Name"].tolist()
    k = count

    # Track judge assignment counts
    judge_counts = defaultdict(int)
    assignments = []
    used_combos = set()

    # Helper function to get a sorted combo of least-assigned judges
    def get_balanced_combo(judges, judge_counts, used_combos, k):
        # Sort by current count (ascending)
        sorted_judges = sorted(judges, key=lambda j: judge_counts[j])
        combos = combinations(sorted_judges, k)
        for combo in combos:
            if tuple(sorted(combo)) not in used_combos:
                return combo
        return None  # fallback if no combo found

    # Assign judges to each project in a balanced way
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

    # Format grouped output
    assignment_df = pd.DataFrame(assignments)
    grouped = assignment_df.groupby("Judge Name")

    formatted_output = []
    for judge, group in grouped:
        formatted_output.append(judge)
        formatted_output.append("--------------------------------")
        formatted_output.append(f"Table      Project")
        for _, row in group.iterrows():
            formatted_output.append(f"{row['Table Number']:<10} {row['Project Name']}")
        formatted_output.append("")

    output = "\n".join(formatted_output)

    # Save to text file
    output_txt_path = "output/judge_assignments.txt"
    with open(output_txt_path, "w") as f:
        f.write(output)
    print(f"[-] Judges assigned to projects successfully...")

    return output


def extract_text(src, file_suffix):
    # Save to file
    if file_suffix == ".":
        with open(f"output/contacts_list", "w") as f:
            f.write(src)
    else:
        with open(f"output/contacts_{file_suffix}", "w") as f:
            f.write(src)


def main():
    parser = argparse.ArgumentParser(description="Process hackathon scores.")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--export", help="Export results to a CSV file")
    parser.add_argument("--contacts", help="Show list of participant's contact info")
    parser.add_argument("--projects", action="store_true", help="Show list of all projects")
    parser.add_argument("--assign", action="store_true", help="Assigns judges to projects for scoring")

    args = parser.parse_args()

    # CSV file path
    file_path = f"data/{args.file}"

    if args.assign:
        print("[-] Parsing project data...")
        df = pd.read_csv(file_path)
        result_text = assign_tables(df)
        print(f"[-] Judge assignment file saved successfully...")

    if args.contacts:
        df = pd.read_csv(file_path)
        print("[-] Parsing contact information...")
        result_text = extract_contacts(df, args.contacts)

        if args.export:
            extract_text(result_text, file_suffix=args.export)
            file_suffix = re.sub(r'[^A-Za-z0-9]', '', args.export)

            # Print to screen
            print("\n" + result_text)
            print(f"[-] File created successfully: contacts_{file_suffix}.txt")

    if args.projects:
        print("[-] Loading project data...")
        df = pd.read_csv(file_path)
        projects = list_projects(df)
        with open("output/projects_list.txt", "w") as f:
            f.write(projects)
        print(f"[-] List of projects saved successfully...")


if __name__ == "__main__":
    main()