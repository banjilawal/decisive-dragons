from pathlib import Path
from game import launch

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    ASSETS = PROJECT_ROOT / 'asset'
    FONT = PROJECT_ROOT / 'font'
    LEVEL = PROJECT_ROOT / 'level'

    launch(
        graphics_dir=ASSETS,
        fonts_dir=FONT,
        levels_dir=LEVEL
    )

