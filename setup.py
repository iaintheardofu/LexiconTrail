"""
Setup configuration for LexiconTrail demo package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lexicontrail-demo",
    version="1.0.0",
    author="The AI Cowboys",
    author_email="m_pendleton@theaicowboys.com",
    description="Demo package for LexiconTrail - Advanced Agentic AI System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iaintheardofu/LexiconTrail",
    project_urls={
        "Bug Tracker": "https://github.com/iaintheardofu/LexiconTrail/issues",
        "Documentation": "https://github.com/iaintheardofu/LexiconTrail/docs",
        "Company": "https://theaicowboys.com",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "llama-index>=0.10.0",
        "openai>=1.0.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "fastapi>=0.100.0",
        "httpx>=0.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.1.0",
            "mkdocstrings>=0.22.0",
        ],
    },
)