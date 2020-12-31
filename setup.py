from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = ''
LONG_DESCRIPTION = ''

setup(
    name='vpos',
    version=VERSION,
    author='Ilton Ingui',
    author_email='ilton@nextbss.co.ao',
    long_description=LONG_DESCRIPTION,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
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