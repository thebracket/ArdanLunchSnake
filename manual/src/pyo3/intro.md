# Introducing PyO3

PyO3 (available at https://github.com/PyO3/pyo3) is a Rust library built
around making it easy to create Rust - and wrap it up in a Python library
with minimal pain.

PyO3 takes advantage of Rust's procedural macro system to let you declaratively
mark Rust modules as Python modules, functions as Python functions - and also supports
Python classes.

The result is code that is still easy to read:

```rust
#[pyo3::pymodule]
mod string_sum {
  use pyo3::prelude::*;

  /// Formats the sum of two numbers as string.
  #[pyfunction]
  fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
  }
}
```

It also supports running/evaluating Python from Rust - but we won't have time for that today.

PyO3 has become my go-to for helping people who have Python performance problems. Once they've
iterated to a solution in Python, PyO3 makes it easy to provide what they need without throwing
away their Python setup.
