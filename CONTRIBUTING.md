# Contributing to Oldy

First off, thank you for considering contributing to Oldy! It's people like you that make open-source tools great.

This document serves as a guide for developers looking to set up the project locally, understand the architecture, and submit pull requests.

## 🛠 Local Development Setup

To get started with developing Oldy:

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/PTBYSR/oldy.git
   cd oldy
   ```

2. **Set up your Python environment:**
   Ensure you are using Python 3.10 or higher.
   ```bash
   # Install Oldy in "editable" mode
   pip install -e .
   ```
   *Note: This will install the necessary dependencies (`typer`, `rich`, `psutil`, `httpx`, `questionary`) and link the `oldy` command globally to your local source code.*

3. **Verify the installation:**
   ```bash
   oldy --help
   ```

## 🏗 Codebase Structure

Oldy is built using **Typer** for the CLI and **Rich** for the terminal UI. 

- `main.py` - The primary entry point.
- `oldy/cli.py` - Defines all the CLI commands (`start`, `stop`, `status`, etc.) and the TUI panels.
- `oldy/hardware.py` - Handles system capability detection (RAM, CPU, OS).
- `oldy/models.py` - Logic for model selection based on system hardware.
- `oldy/ollama_manager.py` - Installs, manages, and interacts with the Ollama background daemon.
- `oldy/tunnel.py` - Handles downloading and interacting with the `ngrok` binary for public URLs.
- `oldy/config.py` - Manages local JSON configurations stored in `~/.oldy/config.json`.

## 📦 Building the Executables

We use **PyInstaller** to bundle Oldy into a standalone executable so non-developers can run it without Python.

**1. Build the standalone `.exe`:**
```bash
pip install pyinstaller
python -m PyInstaller --onefile --name oldy main.py
```
This generates `dist/oldy.exe`.

**2. Build the Windows Installer (`OldySetup.exe`):**
To generate the final Windows installer, download [Inno Setup](https://jrsoftware.org/isdl.php), open the `oldy.iss` file located in the root of the project, and click **Compile**.

## 🚀 Submitting a Pull Request (PR)

1. **Create a branch** for your feature or bug fix: `git checkout -b feature/my-new-feature`
2. **Make your changes** and test them thoroughly. Ensure that commands like `oldy start` and `oldy stop` still handle errors cleanly.
3. **Commit your changes** with a clear and descriptive commit message.
4. **Push the branch** to your fork: `git push origin feature/my-new-feature`
5. **Open a Pull Request** on the main repository.

## 🐛 Bug Reports & Feature Requests

If you don't want to write code but have an idea or found a bug, please [open an issue](https://github.com/PTBYSR/oldy/issues) with detailed steps to reproduce the problem or a clear description of the feature request.

Thank you for contributing!