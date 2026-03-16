# PyO3 Setup - Maturin

There are also a few other steps required to make a modern Python library work. You need to put
it in the right place, follow some wrapping conventions for a "wheel" (so it works on multiple
systems), and adopt a few conventions to make it `pip`-friendly and friendly to other package managers.

Fortunately, a tool named `maturin` exists to automate a lot of the drudgery.

> I keep threatening to tattoo `maturin develop` on my hand. I'm used to Cargo. I keep typing `maturin build`, thinking it will be like `cargo build`. But that builds the entire pip setup rather than actually recompiling, so I'll probably make that mistake today.

Let's walk through setting up Maturin and PyO3.
