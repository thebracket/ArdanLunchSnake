# All About PyResult

You probably noticed that there is `PyResult` everywhere in the code.

```rust
fn sum_as_string(a: usize, b: usize) -> PyResult<String>
```

Python uses an exception based error handling system. Rust doesn't use exceptions at all. Rust
instead uses an enumeration named `Result` (a sum type, or tagged union if you know C).

In Go, you might have a function that returns `(resultType, error)`, and then check
`if err != nil`. Rust is similar, but enumerations occupy exactly as much memory as the largest
element plus a tag (it's literally a tagged union from C). The `Result` enum in Rust is:

```rust
pub enum Result<T, E> {
  Ok(T),
  Err(E)
}
```

Over in Python-land, the language uses exceptions:

```python
def divide(x, y):
    try:
        # Code that might raise an exception
        result = x // y 
    except ZeroDivisionError:
        # Code that runs if a ZeroDivisionError occurs
        print("Error: You are dividing by zero")
    else:
        # Code that runs if NO exception occurs in the try block
        print(f"Yeah! Your answer is: {result}")
    finally:
        # Code that ALWAYS executes, regardless of an exception
        print("This block is always executed")
```

PyO3 bridges the gap between the two. The Rust function will return
a Rust-style success or error code, and PyO3 will map failure into
an exception.

Let's try it. Over in the scratchpad, let's add a function that can
fail:

```rust
#[pymodule]
mod scratchpad {
    use pyo3::exceptions::PyArithmeticError;
    use pyo3::prelude::*;

    #[pyfunction]
    fn divide(a: i32, b: i32) -> PyResult<i32> {
        if b == 0 {
            Err(PyArithmeticError::new_err("Dividing by zero will ruin your day"))
        } else {
            Ok(a / b)
        }
    }
}
```

Notice that the exception import is inside the Rust module created by
`#[pymodule]`. If you import it at the crate root instead, `divide`
won't see it because it lives inside the nested `scratchpad` module.

```rust
use pyo3::exceptions::PyArithmeticError;
```

Build it with `maturin develop` and try the RPL:

```
(.venv) herbert@bertix23:~/Documents/Ardan/LunchLearnPythonRust/code/scratchpad$ python3
Python 3.13.7 (main, Mar  3 2026, 12:19:54) [GCC 15.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import scratchpad
>>> scratchpad.divide(1,2)
0
>>> scratchpad.divide(1,0)
Traceback (most recent call last):
  File "<python-input-2>", line 1, in <module>
    scratchpad.divide(1,0)
    ~~~~~~~~~~~~~~~~~^^^^^
ArithmeticError: Dividing by zero will ruin your day
>>> quit
```
