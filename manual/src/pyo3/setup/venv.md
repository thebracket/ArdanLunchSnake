# Let's Make a Virtual Environment (venv)

> Using JetBrains' Python editor (PyCharm) has made me lazy. I also have a bash alias for this on my regular workstation!

So we change to our scratchpad directory (`code/scratchpad` in the repo) and setup a Python
virtual environment.

```bash
mkdir scratchpad
cd scratchpad
python -m venv .env
source .env/bin/activate
```

We now have our very own virtual environment. Your terminal window should show something like this:

```
(.venv) herbert@bertix23:~/Documents/Ardan/LunchLearnPythonRust/code/scratchpad$
```

> I won't stop you from shouting "Carpe Diem"/"Leeroy Jenkins" and installing everything in your root Python environment. Your OS *hopefully* will.
