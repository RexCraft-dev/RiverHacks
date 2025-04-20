import pandas as pd
import argparse


def load_data(file):
    df = pd.read_csv(file)
    df = df.rename(columns={"Project Name (from Project)": "ProjectName"})
    df = df.rename(columns={"Track Option 1 (from ProjectTable 4)": "Track1"})
    df = df.rename(columns={"Track Option 2 (from ProjectTable 4)": "Track2"})
    new_df = df[["ProjectName", "Innovation", "Value & Impact",
                 "Completeness", "Technical Implementation",
                 "Track1", "Track2", "Cheating"]].copy()
    new_df["overall_rating"] = new_df[["Innovation", "Value & Impact", "Completeness",
                                       "Technical Implementation"]].mean(axis=1)
    return new_df


def get_overall(df, include_overall=True):
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    if include_overall:
        cols.append("overall_rating")
    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()
    grouped = grouped.sort_values(by="overall_rating", ascending=True).reset_index(drop=True)
    grouped.index = grouped.index + 1  # Make index start at 1 instead of 0
    grouped.index.name = "Rank"
    if include_overall:
        grouped = grouped.sort_values(by="overall_rating")
    return grouped


def get_track(df, track, include_overall=True):
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    tracks = ["", "Best Overall", "Best Design", "Cybersecurity", "webAI",
              "Community Engagement", "Community Choice"]

    df = df[(df["Track1"] == tracks[track]) | (df["Track2"] == tracks[track])].copy()

    if include_overall:
        cols.append("overall_rating")

    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()
    grouped = grouped.sort_values(by="overall_rating", ascending=True).reset_index(drop=True)
    grouped.index = grouped.index + 1  # Make index start at 1 instead of 0
    grouped.index.name = "Rank"

    if include_overall:
        grouped = grouped.sort_values(by="overall_rating", ascending=False)

    return grouped


def get_cheat(df):
    return df[df["Cheating"] == "checked"]


def main():
    parser = argparse.ArgumentParser(description="Process hackathon scores.")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--all", action="store_true", help="Export all track and overall results to CSV")
    parser.add_argument("--overall", action="store_true", help="Show top N projects only")
    parser.add_argument("--track", help="Show projects in selected track")
    parser.add_argument("--cheat", action="store_true", help="Show projects suspected of cheating")
    parser.add_argument("--export", help="Export results to a CSV file")

    args = parser.parse_args()

    df = load_data(args.file)
    result_df = df

    if args.overall:
        result_df = get_overall(df, include_overall=True)
        print("\nOverall Results")
        print("------------------------------------------------------------------------------------------------------")
        print(result_df.to_string())

    if args.track:
        result_df = get_track(df, args.track)
        print(f"\nResults for track: {args.track}")
        print("------------------------------------------------------------------------------------------------------")
        print(result_df.to_string())

    if args.cheat:
        result_df = get_cheat(df)
        print("\nSuspected Cheaters")
        print("------------------------------------------------------------------------------------------------------")
        print(result_df["ProjectName"].to_string(index=False))

    if args.all:
        base_export_path = args.export if args.export else "results"

        # Export overall
        overall_df = get_overall(df, include_overall=True)
        overall_df.index.name = "Rank"
        overall_df = overall_df.sort_values(by="overall_rating", ascending=True)
        overall_filename = f"{base_export_path}_overall.txt"
        with open(overall_filename, "w") as f:
            f.write(df.to_string())
        print(f"\nExported overall results to {overall_filename}")

        # Export each track
        tracks = ["Best Design", "Cybersecurity", "webAI",
                  "Community Engagement", "Community Choice"]

        for track in tracks:
            track_df = get_track(df, tracks.index(track))
            track_df.index.name = "Rank"
            track_df = track_df.sort_values(by="overall_rating", ascending=True)
            track_filename = f"{track.replace(' ', '_').lower()}.txt"
            with open(track_filename, "w") as f:
                f.write(track_df.to_string())
            print(f"Exported {track} results to {track_filename}")

    elif args.export:
        result_df.to_csv(args.export, index=False)
        print(f"\nExported results to {args.export}")


if __name__ == "__main__":
    main()
