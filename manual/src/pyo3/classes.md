# Python Classes

Rust isn't an object-oriented language (although you can make it feel that way with traits).
Python is. So PyO3 includes some bridging attributes to allow you to express Rust structures as
Python classes.

The nice part is that the mapping is pretty direct:

- `#[pyclass]` marks the Rust struct as a Python class.
- `#[pymethods]` is where the constructor and methods live.
- `#[new]` becomes Python's constructor.
- `#[pyo3(get)]` exposes a field as a Python attribute.

So if you want a very small example you can point to in a hurry, this works well:

```rust
#[pyclass]
struct Counter {
    #[pyo3(get)]
    count: usize,
}

#[pymethods]
impl Counter {
    #[new]
    fn new(count: usize) -> Self {
        Self { count }
    }

    fn increment(&mut self) {
        self.count += 1;
    }

    fn add(&mut self, amount: usize) {
        self.count += amount;
    }

    fn __repr__(&self) -> String {
        format!("Counter(count={})", self.count)
    }
}
```

Since this example is using the inline `#[pymodule] mod scratchpad { ... }` style, we also
export the class from the module:

```rust
#[pymodule]
mod scratchpad {
    #[pymodule_export]
    use super::Counter;
}
```

Build it with `maturin develop` and try it:

```
(.venv) herbert@bertix23:~/Documents/Ardan/LunchLearnPythonRust/code/scratchpad$ python3
Python 3.13.7 (main, Mar  3 2026, 12:19:54) [GCC 15.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from scratchpad import Counter
>>> c = Counter(10)
>>> c
Counter(count=10)
>>> c.increment()
>>> c.add(5)
>>> c.count
16
>>> quit
```

That's enough to get the idea across:

- A Rust `struct` becomes a Python class.
- Rust methods become Python methods.
- Rust fields can become Python properties.

The full example is in `code/scratchpad/src/lib.rs` in the repo.
