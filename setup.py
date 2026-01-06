"""
Setup script for heart-disease-mlops package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="heart-disease-mlops",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="MLOps pipeline for heart disease prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/heart-disease-mlops",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "train-model=scripts.train_model:main",
        ],
    },
)
