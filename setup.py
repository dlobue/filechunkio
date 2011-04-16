#!/usr/bin/env python
from distutils.core import setup

from filechunkio import __version__


setup(
    name="filechunkio",
    version=unicode(__version__),
    description="FileChunkIO represents a chunk of an OS-level file "\
        "containing bytes data",
    long_description=open("README", 'r').read(),
    author="Fabian Topfstedt",
    author_email="topfstedt@schneevonmorgen.com",
    url="http://bitbucket.org/fabian/filechunkio",
    license="MIT license",
    packages=["filechunkio"],
)
