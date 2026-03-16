# Python is Awesome

I know, I'm a Rust guy. I love speed, elegance, a bit more speed, proper strong typing... although this may not be entirely true, since I also enjoy C#, C, C++, Java, Perl, and more.

But above all, I'm pragmatic. **Use the tool that fits the task at hand**.

And for many things, Python is a *great* tool. It's become pretty much the standard for:

* Prototyping.
* Exploratory programming.
* Teaching your kid to make cool things happen on the screen.
* Data science and AI development.

> It's also *really* well understood by most of the LLM systems out there.

Who wouldn't love:

```python
# from code/python_rocks
python3
>>> import polars as pl
>>> import matplotlib.pyplot as plt
>>> df = pl.read_csv("sample_sales.csv")
>>> df
>>> monthly = (
...     df.group_by("month_number", "month")
...     .agg(pl.col("revenue").sum().alias("revenue"))
...     .sort("month_number")
... )
>>> monthly
>>> plt.bar(monthly["month"].to_list(), monthly["revenue"].to_list())
>>> plt.title("Revenue by Month")
>>> plt.tight_layout()
>>> plt.savefig("sales_by_month.png")
```

> This is in `code/python_rocks`, complete with a `README.md`, `requirements.txt`, and `example.py`.

It's also really nice for things like Jupyter Notebooks, where you can throw some Python at a mostly visual workflow and start *feeling* your data.
