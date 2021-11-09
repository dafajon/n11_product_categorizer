
from setuptools import setup, find_packages

setup(
    author="Dorukhan Afacan",
    author_email="dorukhan.afacan@gmail.com",
    name='n11', 
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where='.'),
    package_dir={"":'.'},
    entry_points={
    'console_scripts': [
        'n11=n11.__main__:cli',
    ],
})
