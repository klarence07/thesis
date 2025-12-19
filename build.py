import PyInstaller.__main__
import os
import shutil

# Define the script to convert
script_path = "main.py"
app_name = "Codeventures"

# Define assets to include
assets = [
    "*.png",
    "*.wav",
    "*.ttf"
]

# Create the add-data argument
# Format: "source;destination" (Windows) or "source:destination" (Linux/Unix)
# Since we want to be cross-platformish but the user is likely on Windows (winsound),
# we will use os.pathsep to be safe, or just assume the user runs this on their platform.
separator = os.pathsep

# Helper to construct the --add-data argument
add_data_args = []
for asset in assets:
    # We want to include files matching the pattern in the root of the output directory
    # So we pass "filename;."
    # But PyInstaller expects exact files or folders.
    # We can rely on PyInstaller to find files if we pass the current directory as source
    pass

# Better approach: List all files explicitly if possible, or use '.'
# Let's list specific files to be clean, or just use "." to include everything in current dir?
# No, that includes source code.

# Let's find all png, wav, ttf files in the directory
import glob
files_to_include = []
for ext in ["png", "wav", "ttf"]:
    files_to_include.extend(glob.glob(f"*.{ext}"))

add_data_options = []
for file in files_to_include:
    # Syntax: source_file:dest_folder
    # On Windows it's source_file;dest_folder
    add_data_options.append(f'--add-data={file}{separator}.')

# Common options
options = [
    script_path,
    '--name=' + app_name,
    '--onefile',
    '--windowed',  # Hide console
    '--clean',
]

# Add data options
options.extend(add_data_options)

print(f"Building {app_name}...")
print("Options:", options)

# Run PyInstaller
PyInstaller.__main__.run(options)

print("Build complete. Check the 'dist' folder.")
