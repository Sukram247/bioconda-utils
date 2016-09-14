# -*- coding: UTF-8 -*-

from setuptools import setup

# load version info
exec(open("bioconda_utils/version.py").read())

setup(
    name='bioconda-utils',
    version=__version__,
    author="Johannes Köster, Ryan Dale, The Bioconda Team",
    description="Utilities for building and managing conda packages",
    license="MIT",
    packages=["bioconda_utils"],
    include_package_data=True,
    data_files=[
        (
            'bioconda_utils',
            [
                'bioconda_utils/bioconda_startup.sh',
            ],
        )
    ],
    install_requires=["argh", "networkx", "pydotplus", "pyyaml", "conda_build", "docker-py", "requests<2.11"],
    entry_points={"console_scripts": [
        "bioconda-utils = bioconda_utils.cli:main",
        "bioconductor_skeleton = bioconda_utils.bioconductor_skeleton:main"
    ]},
    classifiers=[
        "Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3"
    ]
)
