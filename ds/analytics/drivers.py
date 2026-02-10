import pandas as pd
from pathlib import Path

OUT_DIR = Path(__file__).parent / "outputs"
OUT_DIR.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(OUT_DIR / "tips_cleaned.csv")

    # Core metric
    df["tip_pct"] = df["tip"] / df["total_bill"]

    # 1) Candidate drivers and their impact on average tip %
    drivers = []

    def add_driver(name: str, group_col: str):
        g = df.groupby(group_col, observed=True).agg(
            avg_tip_pct=("tip_pct", "mean"),
            avg_total_bill=("total_bill", "mean"),
            n=("tip_pct", "size"),
        ).reset_index()

        spread = float(g["avg_tip_pct"].max() - g["avg_tip_pct"].min())
        drivers.append({"driver": name, "spread_tip_pct": spread})

        g = g.sort_values("avg_tip_pct", ascending=False)
        g.to_csv(OUT_DIR / f"driver_{group_col}_tip_pct.csv", index=False)

    add_driver("Day of week", "day")
    add_driver("Time (Lunch vs Dinner)", "time")
    add_driver("Smoker vs Non-Smoker", "smoker")
    add_driver("Party size", "size")
    add_driver("Sex (use carefully)", "sex")

    drivers_df = pd.DataFrame(drivers).sort_values("spread_tip_pct", ascending=False)
    drivers_df.to_csv(OUT_DIR / "driver_ranking.csv", index=False)

    top3 = drivers_df.head(3)

    # 2) Build a manager-style summary with actions
    lines = []
    lines.append("# DS-2: Top Drivers of Tip % (Manager Summary)\n\n")
    lines.append("## Top 3 Drivers (ranked by tip % spread)\n\n")
    for _, row in top3.iterrows():
        lines.append(f"- **{row['driver']}** (tip % spread: {row['spread_tip_pct']:.2%})\n")

    lines.append("\n## Recommended Actions\n")
    lines.append("### Staffing\n")
    lines.append("- Add more coverage during periods with higher total bills and unstable tip %.\n")
    lines.append("- Ensure experienced staff are scheduled during the most sensitive shifts.\n\n")

    lines.append("### Service Coaching\n")
    lines.append("- Train staff to handle table types linked with lower tip % (example: larger parties).\n")
    lines.append("- Create a quick service checklist for high-risk tables (greeting time, drink refill cadence, bill timing).\n\n")

    lines.append("### Monitoring\n")
    lines.append("- Track outliers weekly: large bills with low tip % to identify service failures or policy issues.\n")
    lines.append("- Use tip % (not tip amount) to compare fairness across shifts.\n")

    (Path(__file__).parent / "drivers_summary.md").write_text("".join(lines), encoding="utf-8")

    print("Created:")
    print("- outputs/driver_ranking.csv")
    print("- outputs/driver_<col>_tip_pct.csv files")
    print("- drivers_summary.md")

if __name__ == "__main__":
    main()
