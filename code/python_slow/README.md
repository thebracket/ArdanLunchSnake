# Python Slow

Small benchmark for the lunch-and-learn.

It generates a CSV of sales orders, reads the same file once with the Python standard library and once with Polars, prints the same summary statistic from both, and reports the timing difference.

## Run it on a Mac

From this directory:

```bash
cd code/python_slow
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 benchmark.py --regenerate
```

That command creates `generated_orders.csv` locally, benchmarks both approaches, and prints the timings.
