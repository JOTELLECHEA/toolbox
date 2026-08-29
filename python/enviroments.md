# Python Environments & Dependency Management

Quick reference for setting up virtual environments, managing dependencies, and working with modern tooling.

## 1. Standard Library Virtual Environments (`venv`)

The built-in way to isolate project dependencies without external tools.

### Create Environment
```bash
python3 -m venv .venv
```

### Activate Environment

```bash
source .venv/bin/activate
```
```bash
deactivate
```
## 2. Pip & Dependency Freezing
Standard package management inside an active virtual environment.

Install Packages
```bash
pip install package_name
Freeze Current Dependencies
Save exact package versions to a requirements file to ensure reproducible builds.
```
```bash
pip freeze > requirements.txt
Install from Requirements
Bash
pip install -r requirements.txt
```
## 3. Common Troubleshooting & Gotchas
Virtualenv not activating in VS Code: Open the command palette (Ctrl+Shift+P or Cmd+Shift+P), search for Python: Select Interpreter, and point it directly to your .venv/bin/python (or Scripts\python.exe on Windows).

Permission Errors (pip install): Ensure your virtual environment is actively sourced. If you see permission errors globally, never use sudo pip install—always use a local venv.