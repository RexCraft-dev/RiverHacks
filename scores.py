import pandas as pd
import argparse
import random
from itertools import combinations
from collections import defaultdict

# Set float precision to 2 for scores
pd.set_option("display.precision", 2)


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
    new_df["Overall Score"] = new_df[["Innovation", "Value & Impact",
                                      "Completeness", "Technical Implementation"]].mean(axis=1)
    return new_df


def get_overall(df, include_overall=True):
    # Prepare the list of columns to average
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    if include_overall:
        cols.append("Overall Score")

    # Group by project name and compute average scores
    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()

    # Rank projects by overall rating (ascending first, then descending if flagged)
    grouped = grouped.sort_values(by="Overall Score", ascending=False).reset_index(drop=True)
    grouped.index = grouped.index + 1
    grouped.index.name = "Rank"

    if include_overall:
        grouped = grouped.sort_values(by="Overall Score", ascending=False)

    return grouped


def get_track(df, track, include_overall=True):
    # List of all valid track names (indexed)
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    tracks = [
        "Main Event",
        "Disaster Response",
        "Accessible City",
        "Cybersecurity",
        "webAI",
        "Mobility Access",
        "Public Safety Insights"
    ]

    # Filter entries where the project is in the selected track
    df = df[(df["Track1"] == tracks[track]) | (df["Track2"] == tracks[track])].copy()

    if df.empty:
        return pd.DataFrame()

    if include_overall:
        cols.append("Overall Score")

    # Group and rank within the track
    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()
    grouped = grouped.sort_values(by="Overall Score", ascending=False).reset_index(drop=True)
    grouped.index = grouped.index + 1
    grouped.index.name = "Rank"

    if include_overall:
        grouped = grouped.sort_values(by="Overall Score", ascending=False)

    return grouped


def get_cheat(df):
    # Return only projects flagged as cheating
    return df[df["Cheating"] == "checked"]


def export_all_results(df, count=None):
    # Export overall rankings
    overall_df = get_overall(df, include_overall=True)
    overall_df = overall_df[["ProjectName", "Overall Score"]]
    overall_df = overall_df.sort_values(by="Overall Score", ascending=False).reset_index(drop=True)
    overall_df.index = overall_df.index + 1
    overall_df.index.name = "Rank"
    overall_filename = f"output/best_overall.txt"
    print("[BEST OVERALL] Parsing results...")

    if count:
        overall_df = overall_df.head(count)

    with open(overall_filename, "w") as f:
        f.write(overall_df.to_string())
        print(f"[SUCCESS] Data written to file...")
    print(f"[SUCCESS] Exported overall results to {overall_filename} successfully...")

    # Export each individual track
    tracks = [
        "Main Event",
        "Disaster Response",
        "Accessible City",
        "Cybersecurity",
        "webAI",
        "Mobility Access",
        "Public Safety Insights"
    ]

    for track in tracks:
        print(f"[{track.upper()}] Parsing results...")
        track_df = get_track(df, tracks.index(track))
        track_df = track_df[["ProjectName", "Overall Score"]]
        track_df = track_df.sort_values(by="Overall Score", ascending=False).reset_index(drop=True)
        track_df.index = track_df.index + 1
        track_df.index.name = "Rank"
        track_filename = f"output/{track.replace(' ', '_').lower()}.txt"

        if count:
            track_df = track_df.head(count)

        with open(track_filename, "w") as f:
            f.write(track_df.to_string())
        print(f"[SUCCESS] Exported {track} results to {track_filename} successfully...")


def list_results(df, output_file="output/list_results.txt", count=None, export=None):
    sections = []

    # Tracks
    tracks = [
        "Main Event",
        "Disaster Response",
        "Accessible City",
        "Cybersecurity",
        "webAI",
        "Mobility Access",
        "Public Safety Insights"
    ]

    for track in tracks:
        print(f"[{track.upper()}] Parsing data...")
        track_df = get_track(df, tracks.index(track))
        track_df = track_df[["ProjectName", "Overall Score"]]
        track_df = track_df.sort_values(by="Overall Score", ascending=False).reset_index(drop=True)
        if count:
            track_df = track_df.head(count)
        track_df.index = track_df.index + 1
        track_df.index.name = "Rank"
        section = (f"\n{track.upper()} RESULTS\n" +
                   "-------------------------------------------------\n" +
                   track_df.to_string())
        if track_df.empty:
            section = (f"\n{track.upper()} RESULTS\n" +
                       "-------------------------------------------------\n" +
                       "No Entries")
        sections.append(section)
        print(f"[SUCCESS] [{track.upper()}] Data loaded successfully...")

    # Display all results
    sections = "\n".join(sections)
    print("\n" + sections)

    if export:
        # Write everything to one file
        with open(output_file, "w") as f:
            f.write(sections)
        print(f"[EXPORT] Exported combined results to {output_file} successfully...")


def assign_tables():
    # Load data
    projects_df = pd.read_csv("data/sample_projects.csv")
    with open("data/judges.txt", "r") as f:
        judges = [line.strip() for line in f.readlines() if line.strip()]

    project_names = projects_df["Project Name"].tolist()
    min_judges_per_project = 3

    # Track judge assignment counts
    judge_counts = defaultdict(int)
    assignments = []
    used_combos = set()

    # Helper function to get a sorted combo of least-assigned judges
    def get_balanced_combo(judges, judge_counts, used_combos, k=3):
        # Sort by current count (ascending)
        sorted_judges = sorted(judges, key=lambda j: judge_counts[j])
        combos = combinations(sorted_judges, k)
        for combo in combos:
            if tuple(sorted(combo)) not in used_combos:
                return combo
        return None  # fallback if no combo found

    # Assign judges to each project in a balanced way
    for i, project in enumerate(project_names, start=1):
        combo = get_balanced_combo(judges, judge_counts, used_combos, k=min_judges_per_project)
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

    # Save to text file
    output_txt_path = "output/judge_assignments.txt"
    with open(output_txt_path, "w") as f:
        f.write("\n".join(formatted_output))


def main():
    parser = argparse.ArgumentParser(description="Process hackathon scores.")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--overall", action="store_true", help="Show overall ratings")
    parser.add_argument("--count", type=int, help="Show top N projects only")
    parser.add_argument("--track", type=int, help="Show projects in selected track")
    parser.add_argument("--cheat", action="store_true", help="Show projects suspected of cheating")
    parser.add_argument("--export", help="Export results to a CSV file")
    parser.add_argument("--exportall", action="store_true", help="Export all track and overall results to CSV")
    parser.add_argument("--list", action="store_true",
                        help="Path to a text file to write combined overall and track results")
    parser.add_argument("--assign", action="store_true", help="Assigns judges to projects for scoring")

    args = parser.parse_args()

    # Load and process input data
    df = load_data(f"data/{args.file}")
    result_df = None

    if args.assign:
        assign_tables()

    # Print overall rankings to console
    if args.overall:
        print("[LOADING] Parsing overall data...")
        result_df = get_overall(df)
        print("Overall Results")
        print("---------------------------------------------------------------------------------------------------")
        print(result_df.to_string())

    # Print selected track results to console
    if args.track:
        tracks = [
            "Main Event",
            "Disaster Response",
            "Accessible City",
            "Cybersecurity",
            "webAI",
            "Mobility Access",
            "Public Safety Insights"
        ]
        print(f"[LOADING] Parsing {tracks[args.track-1]} results...")
        result_df = get_track(df, args.track)
        print(f"Results for track: {tracks[args.track-1].upper()}")
        print("---------------------------------------------------------------------------------------------------")
        if args.count is not None:
            print(result_df.head(args.count).to_string())
        else:
            print(result_df.to_string())

    # Print list of suspected cheating projects
    if args.cheat:
        print("[LOADING] Parsing suspicious projects...")
        result_df = get_cheat(df)
        if not result_df.empty:
            print("[FOUND] Suspicious projects found...")
        print("\nSuspicious Projects")
        print("---------------------------------------------------------------------------------------------------")
        print(result_df["ProjectName"].to_string(index=False))
        print()

    # Exports all tracks into a single file
    if args.list:
        print("[LOADING] Parsing results...")
        if args.export:
            list_results(df, count=args.count, export=True)
        else:
            list_results(df, count=args.count)

    # Select specific file path for exporting data
    if args.export and result_df:
        print("[EXPORT] Exporting data...")
        result_df.to_csv(f"output/{args.export}")
        print(f"[SUCCESS] Exported results to {args.export}")

    # Export all results by track and overall in separate files
    if args.exportall:
        print("[EXPORT] Exporting all result files...")
        export_all_results(df, count=args.count)
        print("[SUCCESS] All result files exported successfully")


if __name__ == "__main__":
    main()
