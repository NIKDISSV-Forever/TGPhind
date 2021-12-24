import setuptools

with open('README.md', encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="TGPhind",

    version="0.1.2",

    author="Nikita (NIKDISSV)",
    author_email="nikdissv.forever@protonmail.com",

    description="Search for articles by title, in telegra.ph and its mirrors.",
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

    python_requires='>=3.6',
)