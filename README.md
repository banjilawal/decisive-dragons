# Decisive Dragons

Decisive Dragons is a Python puzzle game built with Pygame.

To get started, first clone this repository using:

```bash
git clone https://github.com/yourusername/decisive-dragons.git
cd decisive-dragons
```

Next, run the setup script:

```bash
python bootstrap.py
```

This script will automatically create a `.venv` virtual environment, install the required dependencies (like `pygame`), set up folders (`assets`, `font`, `level`, `src`), create `main.py` if it's missing, and finally display instructions for running the game. If everything goes well, you'll see instructions at the end for how to activate the virtual environment and launch the game.

If you run into issues or prefer manual setup, you can do the following instead:

```bash
python -m venv .venv
```

Activate the virtual environment:

- On macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

- On Windows (cmd):
  ```cmd
  .venv\Scripts\activate.bat
  ```

- On Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

Then install dependencies manually:

```bash
pip install -r requirements.txt
```

To run the game, use:

```bash
python main.py
```

If you're using PyCharm, open the project, create a virtual environment when prompted or from the interpreter settings, install the requirements, and run `main.py` from the project tree.

This project requires Python 3.11 or later. To add any new dependencies, install them with pip and then run:

```bash
pip freeze > requirements.txt
```