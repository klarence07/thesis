from setuptools import setup

setup(
    name="Codeventures",
    version="1.0.0",
    description="An RPG-style coding learning game",
    author="Codeventures Team",
    py_modules=["main", "db_utils", "lessons"],  # Include modules explicitly
    install_requires=[
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "codeventures=main:main_entry_point",  # We will need to create this entry point function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
