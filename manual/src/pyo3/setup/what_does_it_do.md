# What does it do?

Let's take a peek at our `src/lib.rs` file:

```rust
use pyo3::prelude::*; // Import PyO3's default exports

/// A Python module implemented in Rust.
#[pymodule]
mod scratchpad {
    use pyo3::prelude::*;

    /// Formats the sum of two numbers as string.
    #[pyfunction]
    fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
        Ok((a + b).to_string())
    }
}
```

So we've declared a *module* named `scratchpad` (matching the directory we're working in), which
exports a *function* named `sum_as_string` - which takes two integers and returns their sum,
as a string.

We can *build* it by typing `maturin develop`. This builds a `target` directory (with all the
Rust compilation artefacts), and does a little magic to make sure that the resultant `.so` file
is in the right place for your virtual environment.

Let's try it in the REPL:

```
(.venv) herbert@bertix23:~/Documents/Ardan/LunchLearnPythonRust/code/scratchpad$ python3
Python 3.13.7 (main, Mar  3 2026, 12:19:54) [GCC 15.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import scratchpad
>>> print(scratchpad.sum_as_string(1,2))
3
>>> quit
```
