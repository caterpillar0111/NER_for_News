import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="NER_for_news",
    version="1.0.5",
    description="It would get some entity in news doc",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/caterpillar0111/NER_for_news",
    author="Chong-Yan, Chen",
    author_email="a0955125075@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["NER_tool"],
    include_package_data=True,
    setup_requires=[],
    install_requires=[],
    
)