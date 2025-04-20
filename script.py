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


def get_aggregated(df, include_overall=True):
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    if include_overall:
        cols.append("overall_rating")
    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()
    if include_overall:
        grouped = grouped.sort_values(by="overall_rating", ascending=False)
    return grouped


def get_track(df, track, include_overall=True):
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    df = df[(df["Track1"] == track) | (df["Track2"] == track)].copy()

    if include_overall:
        cols.append("overall_rating")

    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()

    if include_overall:
        grouped = grouped.sort_values(by="overall_rating", ascending=False)

    return grouped


def main():
    parser = argparse.ArgumentParser(description="Process hackathon scores.")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--overall", type=int, help="Show top N projects only")
    parser.add_argument("--track", help="Show projects in selected track")
    parser.add_argument("--export", help="Export results to a CSV file")

    args = parser.parse_args()

    df = load_data(args.file)
    result_df = df

    if args.overall:
        result_df = get_aggregated(df, include_overall=not args.track)
        result_df = result_df.head(args.overall)
        print(result_df.to_string(index=False))

    if args.track:
        result_df = get_track(df, args.track)
        print(f"Results for track: {args.track}")
        print("------------------------------------------------------------------------------------------------")
        print(result_df.to_string(index=False))

    if args.export:
        result_df.to_csv(args.export, index=False)
        print(f"\nExported to {args.export}")


if __name__ == "__main__":
    main()
