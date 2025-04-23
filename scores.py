import pandas as pd
import argparse

# Set float precision to 2 for scores
pd.set_option("display.precision", 2)


def load_data(file):
    # Load the CSV and rename columns for easier reference
    df = pd.read_csv(file)
    df = df.rename(columns={"Project Name (from Project)": "ProjectName"})
    df = df.rename(columns={"Track Option 1 (from ProjectTable 4)": "Track1"})
    df = df.rename(columns={"Track Option 2 (from ProjectTable 4)": "Track2"})

    # Extract only the relevant columns for scoring and analysis
    new_df = df[["ProjectName", "Judge Name", "Innovation", "Value & Impact",
                 "Completeness", "Technical Implementation",
                 "Track1", "Track2", "Cheating"]].copy()

    # Compute average score across the 4 judging categories
    new_df["Overall Score"] = new_df[["Innovation", "Value & Impact",
                                      "Completeness", "Technical Implementation"]].mean(axis=1)
    return new_df


def get_overall(df, count=None, include_overall=True):
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

    if count:
        grouped = grouped.head(count)

    return grouped


def get_track(df, track, include_overall=True):
    # List of all valid track names (indexed)
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    tracks = [
        "Main Track",
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
    new_df = df[df["Cheating"] == "checked"]
    return new_df["ProjectName"]


def export_all_results(df, count=None):
    # Export overall rankings
    overall_df = get_overall(df, include_overall=True)
    overall_df = overall_df[["ProjectName", "Overall Score"]]
    overall_df = overall_df.sort_values(by="Overall Score", ascending=False).reset_index(drop=True)
    overall_df.index = overall_df.index + 1
    overall_df.index.name = "Rank"
    overall_filename = f"output/best_overall.txt"
    print("[-] Parsing results for BEST OVERALL...")

    if count:
        overall_df = overall_df.head(count)

    with open(overall_filename, "w") as f:
        f.write(overall_df.to_string())
        print(f"[-] Data written to file...")
    print(f"[-] Exported overall results to {overall_filename} successfully...")

    # Export each individual track
    tracks = [
        "Main Track",
        "Disaster Response",
        "Accessible City",
        "Cybersecurity",
        "webAI",
        "Mobility Access",
        "Public Safety Insights"
    ]

    for track in tracks:
        print(f"[-] Parsing results for track: {track.upper()}...")
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
        print(f"[-] Exported {track} results to {track_filename} successfully...")


def list_results(df, count=None, export=None):
    sections = []

    # Tracks
    tracks = [
        "Main Track",
        "Disaster Response",
        "Accessible City",
        "Cybersecurity",
        "webAI",
        "Mobility Access",
        "Public Safety Insights"
    ]

    for track in tracks:
        print(f"[-] Parsing data for track: {track.upper()}...")
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
                       "No Entries\n")
        sections.append(section)
        print(f"[-] [{track.upper()}] Data loaded successfully...")

    # Display all results
    sections = "\n".join(sections)

    if export == "all":
        output_file = "output/list_results.txt"
    else:
        output_file = f"output/{export}.txt"

    if export:
        # Write everything to one file
        with open(output_file, "w") as f:
            f.write(sections)
        print(f"[-] Exported combined results to {output_file} successfully...")


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

    args = parser.parse_args()

    # Load and process input data
    file_path = f"data/{args.file}"
    df = load_data(file_path)
    result_df = pd.DataFrame()

    # Print overall rankings to console
    if args.overall:
        print("[-] Parsing overall data...")
        result_df = get_overall(df, args.count)
        print(f"[-] Overall data found...")

    # Print selected track results to console
    if args.track:
        tracks = [
            "Main Track",
            "Disaster Response",
            "Accessible City",
            "Cybersecurity",
            "webAI",
            "Mobility Access",
            "Public Safety Insights"
        ]
        print(f"[-] Parsing {tracks[args.track-1]} results...")
        result_df = get_track(df, args.track)

    # Print list of suspected cheating projects
    if args.cheat:
        print("[-] Parsing suspicious projects...")
        result_df = get_cheat(df)
        if not result_df.empty:
            print("[!] Suspicious projects found...")

    # Exports all tracks into a single file
    if args.list:
        print("[-] Parsing results...")
        if args.export:
            list_results(df, count=args.count, export=args.export)
        else:
            list_results(df, count=args.count)

    # Select specific file path for exporting data
    if args.export and not result_df.empty:
        print("[-] Exporting data...")

        # Ensure file has .txt extension
        export_path = args.export
        if not export_path.endswith(".txt"):
            export_path = f"{export_path}.txt"

        export_file = f"output/{export_path}"

        # Write nicely formatted text output
        with open(export_file, "w") as f:
            f.write(result_df.to_string(index=True))

        print(f"[-] Exported results to {export_file}")

    # Export all results by track and overall in separate files
    if args.exportall:
        print("[-] Exporting all result files...")
        export_all_results(df, count=args.count)
        print("[-] All result files exported successfully")


if __name__ == "__main__":
    main()
