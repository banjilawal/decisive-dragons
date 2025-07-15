import os
import subprocess
import sys
from pathlib import Path
import argparse

def run_command(command: list):
    """Run a subprocess command and exit on failure."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as error:
        print(f"❌ Error: {error}. Command: {' '.join(command)}")
        sys.exit(1)

def get_venv_python(venv_dir=".venv"):
    return os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "python")

def get_venv_pip(venv_dir=".venv"):
    return os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")

def create_virtual_env(venv_dir=".venv"):
    if not os.path.exists(venv_dir):
        print("🔧 Creating virtual environment...")
        run_command([sys.executable, "-m", "venv", venv_dir])
        print("✅ Virtual environment created.")
    else:
        print("🔁 Virtual environment already exists.")

def install_packages(venv_dir=".venv", packages=None):
    pip_executable = get_venv_pip(venv_dir)
    if not os.path.exists(pip_executable):
        print("❌ Could not find pip in the virtual environment.")
        sys.exit(1)

    if packages is None:
        if Path("requirements.txt").exists():
            print("📦 Installing packages from requirements.txt...")
            run_command([pip_executable, "install", "--upgrade", "pip", "wheel"])
            run_command([pip_executable, "install", "-r", "requirements.txt"])
        else:
            packages = ["pygame"]
            print(f"📦 Installing packages: {', '.join(packages)} ...")
            run_command([pip_executable, "install", "--upgrade", "pip", "wheel", *packages])
    else:
        print(f"📦 Installing packages: {', '.join(packages)} ...")
        run_command([pip_executable, "install", "--upgrade", "pip", "wheel", *packages])

    print("✅ Packages installed.")

def configure_project_structure():
    folders = ["assets", "font", "level", "src"]
    for folder in folders:
        path = Path(folder)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"📁 Created folder: {folder}")
        else:
            print(f"🔁 Folder already exists: {folder}")

    init_file = Path("src/__init__.py")
    if not init_file.exists():
        init_file.touch()
        print("📦 Initialized `src` as a Python package")

def create_main_script():
    main_path = Path("main.py")
    if not main_path.exists():
        print("📝 Creating `main.py`...")
        main_path.write_text('''\
from pathlib import Path
import sys

# Add the src directory to Python path
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from game import launch

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent
    ASSETS = PROJECT_ROOT / 'assets'
    FONT = PROJECT_ROOT / 'font'
    LEVEL = PROJECT_ROOT / 'level'

    launch(
        asset_directory=ASSETS,
        font_directory=FONT,
        level_directory=LEVEL
    )
''')
        print("✅ `main.py` created.")
    else:
        print("🔁 `main.py` already exists.")

def launch_game():
    """Launch the game by running main.py with the virtual env Python."""
    print("🚀 Launching the game...\n")
    run_command([get_venv_python(), "main.py"])

def print_post_setup_instructions():
    print("\n🎉 Setup complete!\n")
    if os.name == "nt":
        print("➡ To activate the virtual environment (cmd):")
        print(r"  .venv\Scripts\activate.bat")
        print("➡ Or for PowerShell:")
        print(r"  .venv\Scripts\Activate.ps1")
    else:
        print("➡ To activate the virtual environment:")
        print("  source .venv/bin/activate")

    print("\n➡ Then run your game with:")
    print("  python main.py")

def main():
    parser = argparse.ArgumentParser(description="Bootstrap the game project.")
    parser.add_argument("--no-run", action="store_true", help="Skip launching the game after setup.")
    args = parser.parse_args()

    print("🚀 Setting up your game project...\n")
    create_virtual_env()
    install_packages()
    configure_project_structure()
    create_main_script()
    print_post_setup_instructions()

    if not args.no_run:
        launch_game()

if __name__ == "__main__":
    main()
