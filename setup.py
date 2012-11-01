import os

from setuptools import setup

def read(fname):
    """
    read the content of the specified file
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def version():
    """
    determine version based on debian/changelog
    """
    with open('debian/changelog', 'r') as changelog:
        first_line = changelog.readline()

        _, rest = first_line.split('(', 1)
        result, _ = rest.split(')', 1)

    return result

setup(
    name="python-derek",
    version=version(),
    author="Dmitry Rozhkov",
    author_email="dmitry.rojkov@gmail.com",
    description="Python client for Derek",
    keywords="derek",
    packages=['derek'],
    entry_points={
        'console_scripts': [
            'drk=derek.cli:main'
        ]
    },
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License"
    ]
)
