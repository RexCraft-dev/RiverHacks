import pandas as pd
import argparse
import re


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

    args = parser.parse_args()

    # CSV file path
    file_path = f"data/{args.file}"

    if args.contacts:
        df = pd.read_csv(file_path)
        print("[LOADING] Parsing contact information...")
        result_text = extract_contacts(df, args.contacts)

        if args.export:
            extract_text(result_text, file_suffix=args.export)
            file_suffix = re.sub(r'[^A-Za-z0-9]', '', args.export)

            # Print to screen
            print("\n" + result_text)
            print(f"[EXPORT] File created successfully: contacts_{file_suffix}.txt")

    if args.projects:
        df = pd.read_csv(file_path)
        projects = list_projects(df)
        print(projects)


if __name__ == "__main__":
    main()