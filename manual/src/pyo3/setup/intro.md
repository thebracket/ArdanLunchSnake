# PyO3 Setup - Maturin

There's also a few other steps required for making a modern Python library work. You need to put
it in the right place, there's some wrapping conventions for a "wheel" (so it works on multiple
systems), and a few conventions required to make it `pip` (and other package manager) friendly.

Fortunately, a tool named `maturin` exists to automate a lot of the drudgery.

> I keep threatening to tattoo `maturin develop` on my hand. I'm used to Cargo. I keep tying `maturin build`, thinking it will be like `cargo build`. But that builds the entire pip setup, rather than actually recompiling. So I'll probably make that mistake today.

Let's walk through setting up Maturin and PyO3.
