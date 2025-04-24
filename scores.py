import os
import pandas as pd
import argparse

pd.set_option("display.precision", 2)


def save_txt_and_csv(df, base_path, filename):
    os.makedirs(base_path, exist_ok=True)
    txt_path = os.path.join(base_path, f"{filename}.txt")
    csv_path = os.path.join(base_path, f"{filename}.csv")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(df.to_string(index=False))
    df.to_csv(csv_path, index=False, float_format="%.2f")


def load_data(file):
    df = pd.read_csv(file)
    for col in ["Track1", "Track2", "Project Name (from Project)"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace("[", "", regex=False)\
                                         .str.replace("]", "", regex=False)\
                                         .str.replace("'", "", regex=False).str.strip()

    df = df.rename(columns={
        "Project Name (from Project)": "ProjectName",
        "Track Option 1 (from ProjectTable 4)": "Track1",
        "Track Option 2 (from ProjectTable 4)": "Track2"
    })

    required_cols = [
        "ProjectName", "Judge Name", "Innovation", "Value & Impact",
        "Completeness", "Technical Implementation", "Track1", "Track2", "Cheating"
    ]
    df = df[[col for col in required_cols if col in df.columns]].copy()
    df["Overall Score"] = df[["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]].mean(axis=1)
    return df


def get_overall(df, count=None):
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation", "Overall Score"]
    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()
    grouped = grouped.sort_values(by="Overall Score", ascending=False).reset_index(drop=True)
    grouped.index = grouped.index + 1
    grouped.index.name = "Rank"
    return grouped.head(count) if count else grouped


def get_track(df, track, include_overall=True):
    cols = ["Innovation", "Value & Impact", "Completeness", "Technical Implementation"]
    if include_overall:
        cols.append("Overall Score")

    tracks = [
        "Main Track", "Disaster Response", "Accessible City", "Cybersecurity",
        "webAI", "Mobility Access", "Public Safety Insights"
    ]
    df = df[(df["Track1"] == tracks[track]) | (df["Track2"] == tracks[track])].copy()
    if df.empty:
        return pd.DataFrame()
    grouped = df.groupby("ProjectName", as_index=False)[cols].mean()
    grouped = grouped.sort_values(by="Overall Score", ascending=False).reset_index(drop=True)
    grouped.index = grouped.index + 1
    grouped.index.name = "Rank"
    return grouped


def export_all_results(df, count=None):
    overall_df = get_overall(df, count)
    if not overall_df.empty:
        save_txt_and_csv(overall_df, "output/judging", "best_overall")

    tracks = [
        "Main Track", "Disaster Response", "Accessible City", "Cybersecurity",
        "webAI", "Mobility Access", "Public Safety Insights"
    ]
    for track in tracks:
        track_df = get_track(df, tracks.index(track))
        if not track_df.empty:
            name = track.replace(" ", "_").lower()
            save_txt_and_csv(track_df, "output/judging", name)


def get_cheat(df):
    if "Cheating" in df.columns:
        return df[df["Cheating"] == True]["ProjectName"]
    else:
        print("[!] Warning: 'Cheating' column not found.")
        return pd.Series([], dtype="str")


def list_results(df, count=None, export=None):
    sections = []

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
        print(f"[*] Parsing data for track: {track.upper()}...")
        track_df = get_track(df, tracks.index(track))

        if not track_df.empty and "Overall Score" in track_df.columns:
            track_df = track_df[["ProjectName", "Overall Score"]]
            track_df = track_df.sort_values(by="Overall Score", ascending=False).reset_index(drop=True)
            if count:
                track_df = track_df.head(count)
            track_df.index = track_df.index + 1
            track_df.index.name = "Rank"
            section = (f"\n{track.upper()} RESULTS\n"
                       "-------------------------------------------------\n"
                       + track_df.to_string())
        else:
            section = (f"\n{track.upper()} RESULTS\n"
                       "-------------------------------------------------\n"
                       "No Entries\n")

        sections.append(section)
        print(f"[-] [{track.upper()}] Data loaded successfully...")

    # Display all results
    sections = "\n".join(sections)

    if export == "all":
        output_file = "output/all_results.txt"
    else:
        output_file = f"output/{export}.txt"

    if export:
        with open(output_file, "w") as f:
            f.write(sections)
        print(f"[-] Exported combined results to {output_file} successfully...")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--overall", action="store_true", help="Show overall rankings")
    parser.add_argument("--count", type=int, help="Limit number of top results shown")
    parser.add_argument("--track", type=int, help="Show results for a specific track index")
    parser.add_argument("--exportall", action="store_true", help="Export all tracks and overall results to files")
    parser.add_argument("--cheat", action="store_true", help="Show projects suspected of cheating")
    parser.add_argument("--list", help="Export combined results to a file (provide filename)")
    parser.add_argument("--export", help="Export the currently displayed results to a file")

    args = parser.parse_args()
    df = load_data(f"data/{args.file}")

    if args.overall:
        overall = get_overall(df, args.count)
        save_txt_and_csv(overall, "output/judging", "overall_scores")

    if args.track is not None:
        track_df = get_track(df, args.track)
        save_txt_and_csv(track_df, "output/judging", "tracks")

    if args.cheat:
        cheaters = get_cheat(df)
        save_txt_and_csv(cheaters, "output/judging", "cheat_list")

    if args.list:
        if args.count:
            list_results(df, args.count)
        else:
            list_results(df)

    if args.exportall:
        export_all_results(df, args.count)


if __name__ == "__main__":
    main()
