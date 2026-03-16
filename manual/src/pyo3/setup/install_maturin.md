# Install Maturin

Now that you have a virtual environment, you can use `pip` to install the `maturin` tool:

```bash
pip install maturin
```

You'll see some pretty package installation text, and hopefully - you now have Maturin installed.

You can make a project with `maturin init`. Select `pyo3` from the list (the others are tools
that can do this, too). It will assure you that it has created a project.

Let's have a look at what we have:

```bash
(.venv) herbert@bertix23:~/Documents/Ardan/LunchLearnPythonRust/code/scratchpad$ tree
.
├── Cargo.toml
├── pyproject.toml
└── src
    └── lib.rs

2 directories, 3 files
```

Rust has appeared! You have the standard Rust library components (a `Cargo.toml` - build manifest),
a `src` directory and a `lib.rs` - indicating that the Rust project is a library.

Let's have a look inside `Cargo.toml`. I've annotated some lines:

```toml
[package]
name = "scratchpad"
version = "0.1.0"
edition = "2024"

[lib]
name = "scratchpad"
crate-type = ["cdylib"] # Build as a C dynamic library.

[dependencies]
pyo3 = "0.27.0" # Depend upon the PyO# project
```

And what's inside `pyproject.toml`?

```toml
[build-system]
requires = ["maturin>=1.12,<2.0"]
build-backend = "maturin"

[project]
name = "scratchpad"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Rust",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]
dynamic = ["version"]
```
