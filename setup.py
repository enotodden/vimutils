#!/usr/bin/env python
from distutils.core import setup

setup(
    name="vimutils",
    version="0.2",
    description="Vim utilities..",
    author="Espen Notodden",
    author_email="enotodden@gmail.com",
    url="http://github.com/enotodden/vimutils",
    packages=[
        'vimutils'
    ],
    scripts=[
        "scripts/vt",
        "scripts/ve",
        "scripts/vs",
        "scripts/vls",
        "scripts/vbls",
        "scripts/vdb",
        "scripts/vds",
        "scripts/vu",
        "scripts/vc"
    ]
)


