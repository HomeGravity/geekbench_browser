from setuptools import setup, find_packages

setup(
    name='geekbench6_api',
    version='1.0',
    description='geekbench6 non-officia api',
    author='HomeGravity',
    author_email='mycoding467@gmail.com',
    packages=find_packages(),
        install_requires=[
        'lxml',
        'aiohttp',
        'bs4'
    ],
)
