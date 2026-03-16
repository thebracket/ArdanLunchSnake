from pathlib import Path

import matplotlib.pyplot as plt
import polars as pl


def main() -> None:
    here = Path(__file__).parent
    data_file = here / "sample_sales.csv"
    chart_file = here / "sales_by_month.png"

    df = pl.read_csv(data_file)
    monthly = (
        df.group_by("month_number", "month")
        .agg(pl.col("revenue").sum().alias("revenue"))
        .sort("month_number")
        .select("month", "revenue")
    )

    print("Monthly revenue:")
    print(monthly)

    plt.figure(figsize=(6, 4))
    plt.bar(monthly["month"].to_list(), monthly["revenue"].to_list(), color="#0f766e")
    plt.title("Revenue by Month")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(chart_file, dpi=150)

    print(f"\nChart written to {chart_file.name}")


if __name__ == "__main__":
    main()
