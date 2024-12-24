from setuptools import setup, find_packages

setup(
    name="driink",
    version="0.1.2",
    description="A lightweight command-line tool to track daily water "
                "consumption and send reminders to stay hydrated",
    author="Guido Accardo",
    author_email="gaccardo@gmail.com",
    url="https://github.com/gaccardo/driink",
    packages=find_packages(include=["driink", "driink.*"]),  # Fixed mismatched quotes
    package_data={
        "driink": ["*.ini", "*.toml"],  # Include INI and TOML files
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "driink=driink.cli:main",  # Defines the CLI entry point
        ]
    },  # Removed trailing comma here
    install_requires=["click", "dynaconf"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)

