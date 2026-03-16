# Add Hello World

Now that we can use `sum_as_string`, let's write another function. We'll be traditional.

Open up `src/lib.rs` in your editor, and add (inside the module):

```rust
#[pyfunction]
fn hello_rust() -> PyResult<()> {
    println!("Hello World from Rust");
    Ok(())
}
```

Now we'll build the project with `maturin develop`.

> I'm going to keep repeating that until I remember it. I promise.

And fire up the REPL again:

```
(.venv) herbert@bertix23:~/Documents/Ardan/LunchLearnPythonRust/code/scratchpad$ python3
Python 3.13.7 (main, Mar  3 2026, 12:19:54) [GCC 15.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import scratchpad
>>> scratchpad.sum_as_string(1,2)
'3'
>>> scratchpad.hello_rust()
Hello World from Rust
>>> quit
```

It's a really ergonomic setup for quickly adding Rust functionality to a Python project.
