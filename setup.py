from setuptools import setup, find_packages

setup(
    name='py_file_select',
    version='0.1',
    packages=find_packages(),
    install_requires=['inquirer','click'],
    entry_points={
        'console_scripts': [
            'py_file_select=source.py_file_select:main',
        ],
    },
    setup_requires=['wheel','setuptools']
)
