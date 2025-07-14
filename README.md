# Decisive Dragons Game

A Python-based game using Pygame.

## Getting Started

### Clone the Repository
1. Open your terminal/command prompt
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/decisive-dragons.git
   cd decisive-dragons
   ```

## General Setup Instructions

### Method 1: Command Line Setup
1. Make sure you have Python 3.13.1 or later installed
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the game:
   ```bash
   python src/main.py
   ```

### Method 2: PyCharm Setup

1. **Open Project in PyCharm**
   - Open PyCharm
   - Go to `File > Open` and select the cloned project folder

2. **Create Virtual Environment**
   - Look for the popup suggesting to create a virtual environment, OR
   - Click on "Python Interpreter" in the bottom right status bar
   - Click "Add Interpreter" > "Add Local Interpreter"
   - Select "Virtualenv" as the environment type
   - Make sure Python 3.13 is selected as the base interpreter
   - Leave the location as default (it should be in your project folder as `.venv`)
   - Click "OK"

3. **Install Dependencies**
   - After the virtual environment is created, PyCharm should detect `requirements.txt`
   - Click "Install Requirements" in the popup, OR
   - Open Terminal in PyCharm (`View > Tool Windows > Terminal`)
   - Run: `pip install -r requirements.txt`

4. **Run the Game**
   - Right-click on `main.py` in the Project Explorer
   - Select "Run 'main'"

### Troubleshooting

If you encounter issues:

1. **Check Python Version**
   - Run `python --version` to ensure you have Python 3.13.1 or later

2. **Virtual Environment Issues**
   - Make sure the virtual environment is activated (you should see `(.venv)` in your terminal)
   - Try removing the `.venv` folder and creating a new virtual environment

3. **PyCharm-specific Issues**
   - Verify the Python interpreter is correctly set in:
     `File > Settings > Project > Python Interpreter`
   - Ensure all dependencies are installed (check the packages list in the interpreter settings)

## Development

To add new dependencies:
1. Activate virtual environment
2. Install package: `pip install package_name`
3. Update requirements: `pip freeze > requirements.txt`

## Requirements

- Python 3.13.1 or higher
- Pygame
- Operating System: Windows/macOS/Linux
