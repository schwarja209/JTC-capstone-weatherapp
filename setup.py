#!/usr/bin/env python3
"""
Setup script for Weather Dashboard application.

This enables proper package installation and development setup.

Usage:
    # Development installation (recommended):
    pip install -e .
    
    # Regular installation:
    pip install .
    
    # Install with development dependencies:
    pip install -e ".[dev]"
"""

from setuptools import setup, find_packages
import os


def read_long_description():
    """Read the long description from README file for package metadata."""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "A satirical weather dashboard application"


# Version management
def get_version():
    """Get version from package __init__.py file."""
    version_file = os.path.join("WeatherDashboard", "__init__.py")
    try:
        with open(version_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"').strip("'")
    except (FileNotFoundError, IndexError):
        pass
    return "0.1.0"  # Fallback version


setup(
    name="WeatherDashboard",
    version=get_version(),
    author="Jacob Schwartz",
    author_email="schwarja209@gmail.com",
    description="A satirical weather dashboard",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/schwarja209/JTC-capstone-weatherapp",
    packages=find_packages(exclude=["tests*", "docs*", "data*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "matplotlib>=3.7.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "pre-commit>=2.10",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "weather-dashboard=WeatherDashboard.main:main",
        ],
    },
    zip_safe=False,
    keywords="weather dashboard satirical humor tkinter",
    project_urls={
        "Source": "https://github.com/schwarja209/JTC-capstone-weatherapp",
        "Documentation": "https://github.com/schwarja209/JTC-capstone-weatherapp/docs",
    },
)