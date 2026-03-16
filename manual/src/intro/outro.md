# Outro

So for *our* Python code, how do we take advantage of the flexibile library-first system
Python gives us - without having to understand the innards of the Boost C++ library
for linking to Python, or write our own C stubs?

There are several routes, but my favorite is [PyO3](https://github.com/PyO3/pyo3)
