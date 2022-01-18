# https://packaging.python.org/en/latest/tutorials/packaging-projects/
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if __name__ == "__main__":

    setup(
        name="cli-wordle",
        version="0.0.1",
        description="Wordle in Terminal",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Ajay Dandge",
        url="https://github.com/er-knight/wordle",
        classifiers=[
            "Environment :: Console",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            "Topic :: Games/Entertainment :: Puzzle Games"
        ],
        license="MIT",
        keywords=["wordle", "terminal"],
        packages=find_packages(),
        python_requires=">=3.7",
        install_requires=[
            # https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html
            "colorama==0.4.4",
            "commonmark==0.9.1",
            "Pygments==2.11.2",
            "pyperclip==1.8.2",
            "rich==10.16.2"
        ],
        package_data={
            # https://setuptools.pypa.io/en/latest/userguide/datafiles.html
            "": ["words.txt"]
        },
        entry_points={
            # https://setuptools.pypa.io/en/latest/userguide/entry_point.html
            "console_scripts": ["wordle = wordle.__main__:main"]
        }
    )
