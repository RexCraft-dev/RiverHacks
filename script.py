import pandas as pd
import argparse
import re


def load_data(file):
    # Load the CSV and rename columns for easier reference
    df = pd.read_csv(file)
    df = df.rename(columns={"Project Name (from Project)": "ProjectName"})
    df = df.rename(columns={"Track Option 1 (from ProjectTable 4)": "Track1"})
    df = df.rename(columns={"Track Option 2 (from ProjectTable 4)": "Track2"})

    # Extract only the relevant columns for scoring and analysis
    new_df = df[["ProjectName", "Innovation", "Value & Impact",
                 "Completeness", "Technical Implementation",
                 "Track1", "Track2", "Cheating"]].copy()

    # Compute average score across the 4 judging categories
    new_df["overall_rating"] = new_df[["Innovation", "Value & Impact", "Completeness",
                                       "Technical Implementation"]].mean(axis=1)
    return new_df


def get_overall(df, include_overall=True):
    # Prepare the list of columns to average
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    if include_overall:
        cols.append("overall_rating")

    # Group by project name and compute average scores
    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()

    # Rank projects by overall rating (ascending first, then descending if flagged)
    grouped = grouped.sort_values(by="overall_rating", ascending=False).reset_index(drop=True)
    grouped.index = grouped.index + 1
    grouped.index.name = "Rank"

    if include_overall:
        grouped = grouped.sort_values(by="overall_rating", ascending=False)

    return grouped


def get_track(df, track, include_overall=True):
    # List of all valid track names (indexed)
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    tracks = ["Best Design", "Cybersecurity", "webAI",
              "Community Engagement", "Community Choice"]

    # Filter entries where the project is in the selected track
    df = df[(df["Track1"] == tracks[track]) | (df["Track2"] == tracks[track])].copy()

    if include_overall:
        cols.append("overall_rating")

    # Group and rank within the track
    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()
    grouped = grouped.sort_values(by="overall_rating", ascending=False).reset_index(drop=True)
    grouped.index = grouped.index + 1
    grouped.index.name = "Rank"

    if include_overall:
        grouped = grouped.sort_values(by="overall_rating", ascending=False)

    return grouped


def get_cheat(df):
    # Return only projects flagged as cheating
    return df[df["Cheating"] == "checked"]


def export_all_results(df, export_path=None, count=None):
    # Export overall rankings
    overall_df = get_overall(df, include_overall=True)
    overall_df = overall_df[["ProjectName", "overall_rating"]]
    overall_df = overall_df.sort_values(by="overall_rating", ascending=False).reset_index(drop=True)
    overall_df.index = overall_df.index + 1
    overall_df.index.name = "Rank"
    overall_filename = f"output/best_overall.txt"
    print("[Best Overall] Parsing results...")

    if count is not None:
        overall_df = overall_df.head(count)

    with open(overall_filename, "w") as f:
        f.write(overall_df.to_string())
    print(f">> Exported overall results to {overall_filename} successfully...")

    # Export each individual track
    tracks = ["Best Design", "Cybersecurity", "webAI",
              "Community Engagement", "Community Choice"]

    for track in tracks:
        print(f"[{track.upper()}] Parsing results...")
        track_df = get_track(df, tracks.index(track))
        track_df = track_df[["ProjectName", "overall_rating"]]
        track_df = track_df.sort_values(by="overall_rating", ascending=False).reset_index(drop=True)
        track_df.index = track_df.index + 1
        track_df.index.name = "Rank"
        track_filename = f"output/{track.replace(' ', '_').lower()}.txt"

        if count is not None:
            track_df = track_df.head(count)

        with open(track_filename, "w") as f:
            f.write(track_df.to_string())
        print(f">> Exported {track} results to {track_filename} successfully...")


def export_tolist_results(df, output_file="output/list_results.txt", count=None):
    sections = []

    # Overall section
    print(f"[BEST OVERALL] Parsing data...")
    overall_df = get_overall(df, include_overall=True)
    overall_df = overall_df[["ProjectName", "overall_rating"]]
    overall_df = overall_df.sort_values(by="overall_rating", ascending=False).reset_index(drop=True)

    if count:
        overall_df = overall_df.head(count)

    overall_df.index = overall_df.index + 1
    overall_df.index.name = "Rank"
    sections.append("BEST OVERALL RESULTS\n" +
                    "-------------------------------------------------\n" +
                    overall_df.to_string())
    print("[BEST OVERALL] Data loaded successfully...")

    # Tracks
    tracks = ["Best Design", "Cybersecurity", "webAI",
              "Community Engagement", "Community Choice"]

    for track in tracks:
        print(f"[{track.upper()}] Parsing data...")
        track_df = get_track(df, tracks.index(track))
        track_df = track_df[["ProjectName", "overall_rating"]]
        track_df = track_df.sort_values(by="overall_rating", ascending=False).reset_index(drop=True)
        if count:
            track_df = track_df.head(count)
        track_df.index = track_df.index + 1
        track_df.index.name = "Rank"
        section = (f"\n{track.upper()} RESULTS\n" +
                   "-------------------------------------------------\n" +
                   track_df.to_string())
        sections.append(section)
        print(f"[{track.upper()}] Data loaded successfully...")

    # Write everything to one file
    with open(output_file, "w") as f:
        f.write("\n".join(sections))

    print(f">> Exported combined results to {output_file} successfully...")


def extract_contacts(df, project="all"):
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
    if project.lower() == "all":
        projects = df["ProjectName"].unique()
        file_suffix = "list"
    else:
        if project not in df["ProjectName"].values:
            print(f"[!] Project '{project}' not found.")
            return
        projects = [project]
        file_suffix = re.sub(r'[^A-Za-z0-9]', '', project)

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

    # Print to screen
    print(full_output)

    # Save to file
    with open(f"output/contacts_{file_suffix}.txt", "w") as f:
        f.write(full_output)

    print(f">> Contacts saved to output/contacts_{file_suffix}.txt")


def main():
    parser = argparse.ArgumentParser(description="Process hackathon scores.")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--overall", action="store_true", help="Show overall ratings")
    parser.add_argument("--count", type=int, help="Show top N projects only")
    parser.add_argument("--track", type=int, help="Show projects in selected track")
    parser.add_argument("--cheat", action="store_true", help="Show projects suspected of cheating")
    parser.add_argument("--export", help="Export results to a CSV file")
    parser.add_argument("--exportall", action="store_true",
                        help="Export all track and overall results to CSV")
    parser.add_argument("--tolist", action="store_true",
                        help="Path to a text file to write combined overall and track results")
    parser.add_argument("--contacts", help="Show list of participant's contact info")

    args = parser.parse_args()

    if args.contacts:
        file_path = f"data/{args.file}"
        df = pd.read_csv(file_path)
        print(">> Parsing contact information...")
        extract_contacts(df, args.contacts)
    else:
        # Load and process input data
        df = load_data(f"data/{args.file}")
        result_df = df

        # Print overall rankings to console
        if args.overall:
            print(">> Parsing overall data...")
            result_df = get_overall(df, include_overall=True)
            print("Overall Results")
            print("---------------------------------------------------------------------------------------------------")
            print(result_df.to_string())

        # Print selected track results to console
        if args.track:
            tracks = ["Best Overall", "Best Design", "Cybersecurity", "webAI",
                      "Community Engagement", "Community Choice"]
            print(f">> Parsing {tracks[args.track-1]} results...")
            result_df = get_track(df, args.track)
            print(f"Results for track: {tracks[args.track-1].upper()}")
            print("---------------------------------------------------------------------------------------------------")
            if args.count is not None:
                print(result_df.head(args.count).to_string())
            else:
                print(result_df.to_string())

        # Print list of suspected cheating projects
        if args.cheat:
            print(">> Parsing suspicious projects...")
            result_df = get_cheat(df)
            if not result_df.empty:
                print("[FOUND] Suspicious projects found...")
            print("\nSuspicious Projects")
            print("---------------------------------------------------------------------------------------------------")
            print(result_df["ProjectName"].to_string(index=False))
            print()

        # Export all results by track and overall in separate files
        if args.exportall:
            print(">> Exporting all result files...")
            export_all_results(df, count=args.count)
            print(">> All result files exported successfully")

        # Select specific file path for exporting data
        elif args.export:
            print(">> Exporting data...")
            result_df.to_csv(f"output/{args.export}")
            print(f">> Exported results to {args.export}")

        # Exports all tracks into a single file
        if args.tolist:
            print(">> Parsing results...")
            export_tolist_results(df, count=args.count)


if __name__ == "__main__":
    main()
