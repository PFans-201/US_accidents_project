"""
Setup configuration for US Accidents and Road Quality Analysis project.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="us-accidents-road-quality",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Analysis of US traffic accidents in relation to road surface quality using OpenStreetMap data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/us-accidents-road-quality",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "black>=23.1.0",
            "pylint>=2.16.0",
            "flake8>=6.0.0",
            "mypy>=1.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "run-pipeline=src.main:main",
        ],
    },
)
