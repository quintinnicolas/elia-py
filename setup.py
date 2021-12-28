from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='elia-py',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/quintinnicolas/elia-py',
    author='Nicolas Quintin',
    author_email='nicolasquintin92@gmail.com',
    description='Python3 client for the webservices of Elia',
    python_requires=">=3.7",
    install_requires=required,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    package_data={
        'entsoe-py': ['LICENSE.txt', 'README.md'],
    },
)
