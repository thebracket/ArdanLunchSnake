import argparse
import csv
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path

import polars as pl


DEFAULT_ROWS = 1_000_000
DEFAULT_ITERATIONS = 5
RANDOM_SEED = 2026

REGIONS = ("North", "South", "East", "West", "Central")
CATEGORIES = ("Widget", "Gadget", "Doohickey", "Service", "Bundle")


@dataclass(frozen=True)
class SalesStats:
    kept_orders: int
    total_revenue: float
    average_revenue: float
    top_region: str
    top_region_revenue: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare pure-Python CSV processing with Polars."
    )
    parser.add_argument(
        "dataset",
        nargs="?",
        default="generated_orders.csv",
        help="Path to the CSV dataset to read. Default: generated_orders.csv",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULT_ROWS,
        help=f"Rows to generate when creating a sample dataset. Default: {DEFAULT_ROWS}",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=DEFAULT_ITERATIONS,
        help=f"Timed runs per approach. Default: {DEFAULT_ITERATIONS}",
    )
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="Always regenerate the sample dataset before benchmarking.",
    )
    return parser


def generate_dataset(path: Path, rows: int) -> None:
    rng = random.Random(RANDOM_SEED)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            (
                "order_id",
                "region",
                "category",
                "units",
                "unit_price",
                "discount_pct",
                "returned",
            )
        )

        for order_id in range(1, rows + 1):
            region = REGIONS[rng.randrange(len(REGIONS))]
            category = CATEGORIES[rng.randrange(len(CATEGORIES))]
            units = rng.randint(1, 12)
            unit_price = round(rng.uniform(8.0, 180.0), 2)
            discount_pct = round(rng.choice((0.0, 0.05, 0.1, 0.15, 0.2, 0.25)), 2)
            returned = 1 if rng.random() < 0.08 else 0
            writer.writerow(
                (
                    order_id,
                    region,
                    category,
                    units,
                    f"{unit_price:.2f}",
                    f"{discount_pct:.2f}",
                    returned,
                )
            )


def ensure_dataset(path: Path, rows: int, regenerate: bool) -> None:
    if regenerate or not path.exists():
        action = "Regenerating" if path.exists() else "Generating"
        print(f"{action} dataset with {rows:,} rows at {path} ...")
        generate_dataset(path, rows)
        print("Dataset ready.\n")


def python_stats(path: Path) -> SalesStats:
    kept_orders = 0
    total_revenue = 0.0
    region_totals: dict[str, float] = {}

    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row["returned"] == "1":
                continue

            units = int(row["units"])
            unit_price = float(row["unit_price"])
            discount_pct = float(row["discount_pct"])
            revenue = units * unit_price * (1.0 - discount_pct)

            kept_orders += 1
            total_revenue += revenue
            region = row["region"]
            region_totals[region] = region_totals.get(region, 0.0) + revenue

    top_region, top_region_revenue = max(
        region_totals.items(),
        key=lambda item: item[1],
        default=("n/a", 0.0),
    )
    average_revenue = total_revenue / kept_orders if kept_orders else 0.0
    return SalesStats(
        kept_orders=kept_orders,
        total_revenue=total_revenue,
        average_revenue=average_revenue,
        top_region=top_region,
        top_region_revenue=top_region_revenue,
    )


def polars_stats(path: Path) -> SalesStats:
    df = pl.read_csv(path)
    delivered = df.filter(pl.col("returned") == 0).with_columns(
        (
            pl.col("units") * pl.col("unit_price") * (1.0 - pl.col("discount_pct"))
        ).alias("revenue")
    )

    summary = delivered.select(
        pl.len().alias("kept_orders"),
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("revenue").mean().alias("average_revenue"),
    ).row(0, named=True)

    top_region = (
        delivered.group_by("region")
        .agg(pl.col("revenue").sum().alias("top_region_revenue"))
        .sort("top_region_revenue", descending=True)
        .row(0, named=True)
    )

    return SalesStats(
        kept_orders=int(summary["kept_orders"]),
        total_revenue=float(summary["total_revenue"]),
        average_revenue=float(summary["average_revenue"]),
        top_region=str(top_region["region"]),
        top_region_revenue=float(top_region["top_region_revenue"]),
    )


def benchmark(label: str, iterations: int, runner) -> tuple[SalesStats, list[float]]:
    runner()
    times: list[float] = []
    stats: SalesStats | None = None

    for _ in range(iterations):
        started = time.perf_counter()
        stats = runner()
        times.append(time.perf_counter() - started)

    assert stats is not None
    print(f"{label}: {sum(times) / len(times):.3f}s average over {iterations} runs")
    return stats, times


def print_stats(label: str, stats: SalesStats) -> None:
    print(label)
    print(f"  Kept orders:          {stats.kept_orders:,}")
    print(f"  Total revenue:        ${stats.total_revenue:,.2f}")
    print(f"  Average order value:  ${stats.average_revenue:,.2f}")
    print(
        f"  Top region:           {stats.top_region} (${stats.top_region_revenue:,.2f})"
    )


def stats_match(left: SalesStats, right: SalesStats) -> bool:
    return (
        left.kept_orders == right.kept_orders
        and left.top_region == right.top_region
        and math.isclose(left.total_revenue, right.total_revenue, rel_tol=1e-9)
        and math.isclose(left.average_revenue, right.average_revenue, rel_tol=1e-9)
        and math.isclose(
            left.top_region_revenue, right.top_region_revenue, rel_tol=1e-9
        )
    )


def main() -> None:
    args = build_parser().parse_args()
    here = Path(__file__).resolve().parent
    dataset = Path(args.dataset)
    if not dataset.is_absolute():
        dataset = here / dataset

    ensure_dataset(dataset, args.rows, args.regenerate)

    print(f"Benchmarking {dataset.name} ({dataset.stat().st_size / 1024 / 1024:.1f} MiB)\n")

    python_result, python_times = benchmark(
        "Pure Python", args.iterations, lambda: python_stats(dataset)
    )
    polars_result, polars_times = benchmark(
        "Polars", args.iterations, lambda: polars_stats(dataset)
    )

    if not stats_match(python_result, polars_result):
        raise RuntimeError("Pure Python and Polars produced different results.")

    print()
    print_stats("Shared result:", python_result)

    python_average = sum(python_times) / len(python_times)
    polars_average = sum(polars_times) / len(polars_times)
    speedup = python_average / polars_average

    print("\nTiming summary")
    print(f"  Pure Python average:  {python_average:.3f}s")
    print(f"  Polars average:       {polars_average:.3f}s")
    print(f"  Speedup:              {speedup:.1f}x faster with Polars")


if __name__ == "__main__":
    main()
