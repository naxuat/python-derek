import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-derek",
    version = "0.0.1",
    author = "Dmitry Rozhkov",
    author_email = "dmitry.rojkov@gmail.com",
    description = ("Python client for Derek"),
    license = "GPL",
    keywords = "derek",
    packages=['derek'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPL License",
    ]
)
