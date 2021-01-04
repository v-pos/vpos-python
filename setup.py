from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Facilitates the intereaction with Vpos API'
LONG_DESCRIPTION = open("README.md").read()

setup(
    name='vpos',
    version=VERSION,
    author='Ilton Ingui',
    author_email='ilton@nextbss.co.ao',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url="https://pypi.org/project/vpos/",
    install_requires=[
        "pytest",
        "requests"
    ],
    tests_require=['pytest'],
    keywords=['nextbss', 'python', 'vpos', 'point of sales'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
    
)