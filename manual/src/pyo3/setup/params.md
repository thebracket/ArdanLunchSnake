# Passing Rust Types as Parameters

You have also noticed that we've been passing in `i32`, `usize`, and `String` without doing
any conversion work. PyO3 can handle converting the majority of types into types that Python
can work with (and vice versa). So when you pass a `String` back and forth, you don't have to
remember to work with Python's string representation, C's string representation, etc.

This also applies to a lot of the built-in collections. For example, vectors:

```rust
    #[pyfunction]
    fn vectors(v: Vec<i32>) -> PyResult<Vec<i32>> {
        Ok(v.into_iter().map(|n| n * 2).collect())
    }
```

(This is a function that uses Rust's - admittedly acquired taste - of an iterator transform
to double every item in the vector, consuming the original vector rather than messing with
pointers and references)

```
(.venv) herbert@bertix23:~/Documents/Ardan/LunchLearnPythonRust/code/scratchpad$ python3
Python 3.13.7 (main, Mar  3 2026, 12:19:54) [GCC 15.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import scratchpad
>>> scratchpad.vectors([1,2,3,4,5])
[2, 4, 6, 8, 10]
>>> quit
```

Since Python is dictionary-based, `HashMap` works just as nicely:

```rust
    use std::collections::HashMap;
    #[pyfunction]
    fn mappy(m: HashMap<String, String>) {
        println!("{m:?}");
    }
```

```
(.venv) herbert@bertix23:~/Documents/Ardan/LunchLearnPythonRust/code/scratchpad$ python3
Python 3.13.7 (main, Mar  3 2026, 12:19:54) [GCC 15.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import scratchpad
>>> a={ "key":"value"}
>>> scratchpad.mappy(a)
{"key": "value"}
>>> quit
```
