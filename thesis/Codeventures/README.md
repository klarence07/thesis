# Codeventures

Codeventures is an RPG-style coding learning game built with Python and Tkinter.

## Setup and Installation

### Prerequisites

*   Python 3.6 or higher installed on your system.
*   `pip` (Python package manager).

### Installation

1.  Navigate to the project directory:
    ```bash
    cd thesis/Codeventures
    ```

2.  Install the game and its dependencies:
    ```bash
    pip install .
    ```

    Alternatively, you can install the dependencies manually:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Game

To play the game from the source code, run the `main.py` script:

```bash
python main.py
```

If you installed via `pip install .`, you can also run the game using the command:
```bash
codeventures
```

## Building the Standalone Application

You can package the game into a standalone executable (for Windows/Linux/macOS) using the provided build script.

1.  Ensure you have installed the requirements (specifically `pyinstaller`, which is included in `requirements.txt`).

2.  Run the build script:
    ```bash
    python build.py
    ```

3.  Once the build process completes, you will find the executable in the `dist` folder:
    *   **Windows**: `dist/Codeventures.exe`
    *   **Linux/Mac**: `dist/Codeventures`

You can move this executable to any location on your computer and run it without needing Python installed.

## Features

*   **RPG Gameplay**: Explore a map, fight enemies, and solve coding questions.
*   **Save/Load System**: Progress is saved automatically.
*   **Leaderboard**: Compete for the highest score and fastest time.
*   **Inventory & Crafting**: Collect items and craft upgrades.

## Troubleshooting

*   **Audio**: If you are not on Windows, audio features might be disabled to prevent compatibility issues.
*   **Database**: The game uses a local SQLite database (`codeventures.db`) which is created automatically upon the first run.
