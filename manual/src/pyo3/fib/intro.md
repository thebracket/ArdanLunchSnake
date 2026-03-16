# Fibonacci Numbers - Slow!

We've talked quite a bit about how ergonomic PyO3 makes it to include some Rust in your Python
experience. We haven't really talked much about *why* you might want to do this.

There's actually a bunch of reasons:

* It can be really helpful for integration with larger systems. For example, LibreQoS links a ton of Rust API functions to PyO3 for consumption in Python scripts. Many of our users love writing Python and aren't really ready for Rust.
* Safety. You can make a real mess with multi-threaded Python. Rust lets you have some fearless concurrency.
* Speed.

We're going to play with the latter today.
