import pandas as pd
import argparse


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
    grouped = grouped.sort_values(by="overall_rating", ascending=True).reset_index(drop=True)
    grouped.index = grouped.index + 1
    grouped.index.name = "Rank"

    if include_overall:
        grouped = grouped.sort_values(by="overall_rating")

    return grouped


def get_track(df, track, include_overall=True):
    # List of all valid track names (indexed)
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    tracks = ["", "Best Overall", "Best Design", "Cybersecurity", "webAI",
              "Community Engagement", "Community Choice"]

    # Filter entries where the project is in the selected track
    df = df[(df["Track1"] == tracks[track]) | (df["Track2"] == tracks[track])].copy()

    if include_overall:
        cols.append("overall_rating")

    # Group and rank within the track
    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()
    grouped = grouped.sort_values(by="overall_rating", ascending=True).reset_index(drop=True)
    grouped.index = grouped.index + 1
    grouped.index.name = "Rank"

    if include_overall:
        grouped = grouped.sort_values(by="overall_rating", ascending=False)

    return grouped


def get_cheat(df):
    # Return only projects flagged as cheating
    return df[df["Cheating"] == "checked"]


def export_all_results(df, export_path=None, count=None):
    base_export_path = export_path if export_path else "results"

    # Export overall rankings
    overall_df = get_overall(df, include_overall=True)
    overall_df = overall_df[["ProjectName", "overall_rating"]]
    overall_df = overall_df.sort_values(by="overall_rating", ascending=False).reset_index(drop=True)
    overall_df.index = overall_df.index + 1
    overall_df.index.name = "Rank"
    overall_filename = f"{base_export_path}_overall.txt"

    if count is not None:
        overall_df = overall_df.head(count)

    with open(overall_filename, "w") as f:
        f.write(overall_df.to_string())
    print(f"\nExported overall results to {overall_filename}")

    # Export each individual track
    tracks = ["Best Design", "Cybersecurity", "webAI",
              "Community Engagement", "Community Choice"]

    for track in tracks:
        track_df = get_track(df, tracks.index(track))
        track_df = track_df[["ProjectName", "overall_rating"]]
        track_df = track_df.sort_values(by="overall_rating", ascending=False).reset_index(drop=True)
        track_df.index = track_df.index + 1
        track_df.index.name = "Rank"
        track_filename = f"{track.replace(' ', '_').lower()}.txt"

        if count is not None:
            track_df = track_df.head(count)

        with open(track_filename, "w") as f:
            f.write(track_df.to_string())
        print(f"Exported {track} results to {track_filename}")


def export_inline_results(df, output_file, count=None):
    sections = []

    # Overall section
    overall_df = get_overall(df, include_overall=True)
    overall_df = overall_df[["ProjectName", "overall_rating"]]
    overall_df = overall_df.sort_values(by="overall_rating", ascending=False).reset_index(drop=True)
    if count:
        overall_df = overall_df.head(count)
    overall_df.index = overall_df.index + 1
    overall_df.index.name = "Rank"
    sections.append("OVERALL RESULTS\n" + overall_df.to_string())

    # Tracks
    tracks = ["Best Design", "Cybersecurity", "webAI",
              "Community Engagement", "Community Choice"]

    for track in tracks:
        track_df = get_track(df, tracks.index(track))
        track_df = track_df[["ProjectName", "overall_rating"]]
        track_df = track_df.sort_values(by="overall_rating", ascending=False).reset_index(drop=True)
        if count:
            track_df = track_df.head(count)
        track_df.index = track_df.index + 1
        track_df.index.name = "Rank"
        section = f"\n\n{track.upper()} RESULTS\n" + track_df.to_string()
        sections.append(section)

    # Write everything to one file
    with open(output_file, "w") as f:
        f.write("\n".join(sections))

    print(f"\nExported combined results to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Process hackathon scores.")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--overall", action="store_true", help="Show overall ratings")
    parser.add_argument("--count", type=int, help="Show top N projects only")
    parser.add_argument("--track", help="Show projects in selected track")
    parser.add_argument("--cheat", action="store_true", help="Show projects suspected of cheating")
    parser.add_argument("--export", help="Export results to a CSV file")
    parser.add_argument("--exportall", action="store_true",
                        help="Export all track and overall results to CSV")
    parser.add_argument("--inline", help="Path to a text file to write combined overall and track results")

    args = parser.parse_args()

    # Load and process input data
    df = load_data(args.file)
    result_df = df

    # Print overall rankings to console
    if args.overall:
        result_df = get_overall(df, include_overall=True)
        print("\nOverall Results")
        print("------------------------------------------------------------------------------------------------------")
        print(result_df.to_string())

    # Print selected track results to console
    if args.track:
        result_df = get_track(df, args.track)
        print(f"\nResults for track: {args.track}")
        print("------------------------------------------------------------------------------------------------------")
        print(result_df.to_string())

    # Print list of suspected cheating projects
    if args.cheat:
        result_df = get_cheat(df)
        print("\nSuspected Cheaters")
        print("------------------------------------------------------------------------------------------------------")
        print(result_df["ProjectName"].to_string(index=False))

    # Export all results by track and overall
    if args.exportall:
        export_all_results(df, count=args.count)
        print("Result files exported successfully")

    # If only --export is used, export the last viewed result set
    elif args.export:
        result_df.to_csv(args.export)
        print(f"\nExported results to {args.export}")

    if args.inline:
        export_inline_results(df, args.inline, count=args.count)


if __name__ == "__main__":
    main()
