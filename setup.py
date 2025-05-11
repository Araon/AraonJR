"""
Setup script for AraonJR Discord Bot
"""
from setuptools import find_packages, setup

setup(
    name="araon-jr",
    version="2.0.0",
    description="AraonJR Discord Bot - Modernized version",
    author="Araon",
    packages=find_packages(),
    install_requires=[
        "discord.py>=2.3.2",
        "PyNaCl>=1.5.0",
        "python-dotenv>=1.0.0",
        "wavelink>=1.3.2",
        "requests>=2.31.0",
        "pillow>=10.0.0",
        "wikipedia>=1.4.0",
        "textblob>=0.17.1"
    ],
    python_requires=">=3.12",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "araon-bot=bot:main",
        ],
    },
)
