from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="amazon-wholesale-automation",
    version="1.0.0",
    author="asifceo1",
    description="Automated system for Amazon wholesale product research and distributor discovery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asifceo1/amazon-wholesale-automation",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.1.0",
        "pyyaml>=6.0",
        "sqlalchemy>=2.0",
        "beautifulsoup4>=4.12",
    ],
)
