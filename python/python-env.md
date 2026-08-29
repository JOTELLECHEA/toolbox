# Python Environments

## venv
- `python3 -m venv .venv` — create
- `source .venv/bin/activate` — activate (Linux/Mac)
- `deactivate` — leave the active virtual environment
- `pip freeze > requirements.txt` — snapshot exact installed versions
- `pip install -r requirements.txt` — restore from snapshot

## pip
- `pip install <pkg>` — install a package
- `pip install -e .` — editable install, for developing a local package
- `pip list --outdated` — show packages with newer versions available
- `pip show <pkg>` — version, location, dependencies
- `pip install <pkg>==<version>` — pin a specific version

## conda
- `conda create -n <name> python=3.11` — create a new environment
- `conda activate <name>` — activate an environment
- `conda deactivate` — leave the active environment
- `conda env list` — list all environments
- `conda env export > environment.yml` — snapshot full env (more than pip freeze captures)
- `conda env create -f environment.yml` — restore from snapshot
- `conda install -c conda-forge <pkg>` — install from conda-forge channel
- `conda remove -n <name> --all` — delete an environment entirely

## Sanity checks
- `which python` — confirm which interpreter is actually active
- `python -m pip --version` — confirm pip is tied to the interpreter you expect
- `python -c "import sys; print(sys.prefix)"` — confirm which env Python is running from

## Gotchas
- `pip install` inside a conda env works, but mixing conda and pip for the same
  package can cause dependency resolution conflicts — prefer one or the other per package.
- Forgetting to activate before `pip install` silently installs to the wrong (often global) environment.
