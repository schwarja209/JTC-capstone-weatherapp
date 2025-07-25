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

from typing import Dict
from setuptools import setup, find_packages
import os


def read_long_description() -> str:
    """Read the long description from README file for package metadata."""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "A satirical dual-themed weather dashboard application with real-time weather data"


# metadata management
def get_package_metadata() -> Dict[str, str]:
    """Get metadata using importlib for robust extraction."""
    try:
        # Try to import and get version dynamically
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "weather_init", 
            os.path.join("WeatherDashboard", "__init__.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return {
            'version': getattr(module, '__version__', '0.2.1'),
            'author': getattr(module, '__author__', 'Jacob Schwartz'),
            'email': getattr(module, '__email__', 'schwarja209@gmail.com'),
            'description': getattr(module, '__description__', 'A satirical weather dashboard')
        }
    except Exception:
        # Fallback to hardcoded values
        return {
            'version': '0.2.1',
            'author': 'Jacob Schwartz', 
            'email': 'schwarja209@gmail.com',
            'description': 'A satirical weather dashboard'
        }


metadata = get_package_metadata()
setup(
    name="WeatherDashboard",
    version=metadata.get('version', '0.2.1'),
    author=metadata.get('author', 'Jacob Schwartz'),
    author_email=metadata.get('email', 'schwarja209@gmail.com'),
    description=metadata.get('description', 'A satirical weather dashboard'),
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/schwarja209/JTC-capstone-weatherapp",
    packages=find_packages(exclude=["tests*", "docs*", "data*"]),
    classifiers=[
        "Development Status :: Alpha",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Desktop Environment",
        "Topic :: Satire",
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
            "black>=23.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
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