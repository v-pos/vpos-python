from setuptools import setup, find_packages

VERSION = '1.0'
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
    install_requires=open('requirements.txt').readlines(),
    tests_require=['pytest'],
    keywords=['nextbss', 'python', 'vpos', 'point of sales', 'emis'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
    
)
