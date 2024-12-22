from setuptools import setup, find_packages

setup(
    name="driink",
    version="0.1.0",
    description="A lightweight command-line tool to track daily water"
    "consumption and send reminders to stay hydrated",
    author="Guido Accardo",
    author_email="gaccardo@gmail.com",
    url="https://github.com/gaccardo/driink",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "driink=driink.cli:main",
        ],
    },
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
