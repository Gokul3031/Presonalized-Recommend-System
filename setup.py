from setuptools import setup

with open("Readme.md","r", encoding="utf-8")as f:
    long_description = f.read()

SRC_REPO="src"
LIST_OF_REQUIREMENTS =['streamlit','numpy']

setup(
    name=SRC_REPO,
    version="0.0.1",
    packages=[SRC_REPO],
    python_requirements=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)