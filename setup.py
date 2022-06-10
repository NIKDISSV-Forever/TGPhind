from __future__ import annotations

import setuptools

with open('README.md', encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="TGPhind",

    version="1.0.0",

    author="Nikita (NIKDISSV)",
    author_email="nikdissv@proton.me",

    description="Development Status :: 5 - Production/Stable",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/NIKDISSV-Forever/TGPhind",

    packages=setuptools.find_packages(),

    classifiers=[
        'Programming Language :: Python :: 3.9.7',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    python_requires='>=3.8',
)
