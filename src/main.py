from pathlib import Path
from game import launch

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    ASSETS = PROJECT_ROOT / 'assets'
    FONT = PROJECT_ROOT / 'font'
    LEVEL = PROJECT_ROOT / 'level'

    launch(
        asset_directory=ASSETS,
        font_directory=FONT,
        level_directory=LEVEL
    )

