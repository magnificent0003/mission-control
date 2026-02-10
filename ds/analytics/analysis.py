import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT_DIR = Path(__file__).parent / "outputs"
OUT_DIR.mkdir(exist_ok=True)

def main():
    # Dataset: built-in, no downloads
    df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")

    # Basic cleaning (demo-level but real)
    df.columns = [c.strip().lower() for c in df.columns]
    df["sex"] = df["sex"].astype("category")
    df["smoker"] = df["smoker"].astype("category")
    df["day"] = df["day"].astype("category")
    df["time"] = df["time"].astype("category")

    # Feature engineering
    df["tip_pct"] = df["tip"] / df["total_bill"]

    # Save cleaned data
    cleaned_path = OUT_DIR / "tips_cleaned.csv"
    df.to_csv(cleaned_path, index=False)

    # KPIs
    kpi = {
        "rows": len(df),
        "avg_total_bill": float(df["total_bill"].mean()),
        "avg_tip": float(df["tip"].mean()),
        "avg_tip_pct": float(df["tip_pct"].mean()),
    }

    # Group summaries
    by_day = df.groupby("day", observed=True).agg(
        avg_total_bill=("total_bill", "mean"),
        avg_tip=("tip", "mean"),
        avg_tip_pct=("tip_pct", "mean"),
        n=("total_bill", "size"),
    ).reset_index()

    by_time = df.groupby("time", observed=True).agg(
        avg_total_bill=("total_bill", "mean"),
        avg_tip=("tip", "mean"),
        avg_tip_pct=("tip_pct", "mean"),
        n=("total_bill", "size"),
    ).reset_index()

    by_smoker = df.groupby("smoker", observed=True).agg(
        avg_total_bill=("total_bill", "mean"),
        avg_tip=("tip", "mean"),
        avg_tip_pct=("tip_pct", "mean"),
        n=("total_bill", "size"),
    ).reset_index()

    # Save summaries
    by_day.to_csv(OUT_DIR / "summary_by_day.csv", index=False)
    by_time.to_csv(OUT_DIR / "summary_by_time.csv", index=False)
    by_smoker.to_csv(OUT_DIR / "summary_by_smoker.csv", index=False)

    # Charts (no fancy styling)
    ax1 = by_day.set_index("day")["avg_tip_pct"].plot(kind="bar", title="Average Tip % by Day")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "chart_tip_pct_by_day.png")
    plt.close()

    ax2 = by_time.set_index("time")["avg_total_bill"].plot(kind="bar", title="Average Total Bill by Time")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "chart_total_bill_by_time.png")
    plt.close()

    ax3 = df.plot.scatter(x="total_bill", y="tip", title="Tip vs Total Bill")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "chart_tip_vs_total_bill.png")
    plt.close()

    # Write a short report
    report_lines = []
    report_lines.append("# Tips Dataset: Quick Analytics Report\n")
    report_lines.append("## KPIs\n")
    report_lines.append(f"- Rows: {kpi['rows']}\n")
    report_lines.append(f"- Avg total bill: {kpi['avg_total_bill']:.2f}\n")
    report_lines.append(f"- Avg tip: {kpi['avg_tip']:.2f}\n")
    report_lines.append(f"- Avg tip %: {kpi['avg_tip_pct']:.2%}\n")

    best_day = by_day.sort_values("avg_tip_pct", ascending=False).iloc[0]["day"]
    best_time = by_time.sort_values("avg_total_bill", ascending=False).iloc[0]["time"]

    report_lines.append("\n## Insights (plain language)\n")
    report_lines.append(f"- Highest average tip % day: **{best_day}**\n")
    report_lines.append(f"- Highest average total bill time: **{best_time}**\n")
    report_lines.append("- Tip generally increases as total bill increases (see scatter plot).\n")

    report_lines.append("\n## Files created\n")
    report_lines.append("- outputs/tips_cleaned.csv\n")
    report_lines.append("- outputs/summary_by_day.csv\n")
    report_lines.append("- outputs/summary_by_time.csv\n")
    report_lines.append("- outputs/summary_by_smoker.csv\n")
    report_lines.append("- outputs/chart_tip_pct_by_day.png\n")
    report_lines.append("- outputs/chart_total_bill_by_time.png\n")
    report_lines.append("- outputs/chart_tip_vs_total_bill.png\n")

    (OUT_DIR.parent / "report.md").write_text("".join(report_lines), encoding="utf-8")

    print("Done. Check ds/analytics/outputs and report.md")

if __name__ == "__main__":
    main()
