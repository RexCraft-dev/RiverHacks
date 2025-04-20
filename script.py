import pandas as pd
import argparse


def load_data(file):
    df = pd.read_csv(file)
    df = df.rename(columns={"Project Name (from Project)": "ProjectName"})
    new_df = df[["ProjectName", "Innovation", "Value & Impact",
                 "Completeness", "Technical Implementation", "Cheating"]].copy()
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


def main():
    parser = argparse.ArgumentParser(description="Process hackathon scores.")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--overall", type=int, help="Show top N projects only")
    parser.add_argument("--cat", action="store_true", help="Exclude overall rating from output")
    parser.add_argument("--export", help="Export results to a CSV file")

    args = parser.parse_args()

    df = load_data(args.file)
    result_df = get_aggregated(df, include_overall=not args.cat)

    if args.overall:
        result_df = result_df.head(args.overall)

    print(result_df.to_string(index=False))

    if args.export:
        result_df.to_csv(args.export, index=False)
        print(f"\nExported to {args.export}")


if __name__ == "__main__":
    main()
