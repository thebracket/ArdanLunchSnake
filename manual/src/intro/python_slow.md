# Python can be Slow

That example is pretty nice. A few lines of code, and your data science guy has graphs
and is happy.

Did you notice that all of the hard work is done with [Polars](https://pola.rs/)?

Python is built from the ground up to work with C dynamic libraries that only have to do a little
bit of extra work to function as Python modules. Polars is written in Rust. NumPy is written
in a fun mixture of C, C++ and Fortran. You absolutely *can* write a complete DataFrame,
numerics and analysis system in pure Python. But it will be just a little slow.

> Code example in the `code/python_slow` directory.

On a generated 1,000,000-row CSV (about 35.7 MiB), the pure Python version
uses the standard library `csv` reader to scan the file and calculate a small
sales summary:

* Kept orders: 920,049
* Total revenue: $491,273,673.45
* Average order value: $533.96
* Top region: West

Running the same calculation 5 times on the same dataset gave these averages:

* Pure Python: 1.136 seconds
* Polars: 0.049 seconds
* Result: Polars was about 23.2x faster

> Exact timings will vary by machine, but the gap is usually dramatic.
