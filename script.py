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
    parser.add_argument("--overall", type=int, help="Show top N projects only")
    parser.add_argument("--track", type=int, help="Show projects in selected track")
    parser.add_argument("--cheat", action="store_true", help="Show projects suspected of cheating")
    parser.add_argument("--export", help="Export results to a CSV file")

    args = parser.parse_args()

    df = load_data(args.file)
    result_df = df

    if args.overall:
        result_df = get_overall(df, include_overall=True)
        if args.overall > 0:
            result_df = result_df.head(args.overall)
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
        print(result_df["ProjectName"].to_string(index=False))

    if args.export:
        result_df.to_csv(args.export, index=False)
        print(f"\nExported to {args.export}")


if __name__ == "__main__":
    main()
