from setuptools import setup

setup(
    name='dmenutrello',
    version='0.1.0',
    packages=['dmenutrello'],
    author="Lukas Jurk",
    author_email="ljurk@pm.me",
    description="brings trello to dmenu",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="GPLv3",
    keywords="trello dmenu",
    url="https://github.com/ljurk/dmenutrello",
    entry_points={
        'console_scripts': ['dmenutrello=dmenutrello.dmenutrello:main']
    },
    install_requires=[
        "dmenu",
        "configparser",
        "py-trello"
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ]
)
