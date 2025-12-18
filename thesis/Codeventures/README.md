# Codeventures Setup and Build Guide

This guide explains how to set up the environment, run the application, and build a standalone executable for Codeventures.

## Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

## Installation

1.  **Clone the repository:**
    (If you haven't already)

2.  **Navigate to the project directory:**
    ```bash
    cd thesis/Codeventures
    ```

3.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```
    This will install `Pillow` (for image processing) and `pyinstaller` (for building the executable).

## Running the Application

To run the game from the source code:

```bash
python main.py
```

## Building the Executable

To create a standalone executable that includes all necessary assets (images, sounds, etc.):

1.  **Run the build script:**
    ```bash
    python build.py
    ```

2.  **Locate the executable:**
    After the build process completes, the executable will be located in the `dist` folder:
    `thesis/Codeventures/dist/Codeventures` (or `Codeventures.exe` on Windows).

3.  **Run the executable:**
    You can run this file directly without needing Python installed on the target machine.

## Troubleshooting

-   **UI Won't Load / Crash on Startup:**
    Ensure you have run `pip install -r requirements.txt`.
    If running from source on Linux/macOS, ensure the asset filenames match case-sensitively (e.g., `Npc.png`). The latest code includes fixes for this.

-   **Build Failures:**
    Ensure `PyInstaller` is installed correctly. If `build.py` fails, check the console output for missing hooks or dependency errors.
