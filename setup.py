from setuptools import setup, find_packages

setup(
    name='py_file_select',
    version='0.1',
    packages=find_packages(),
    install_requires=['inquirer==3.4.0','click==8.1.7'],
    entry_points={
        'console_scripts': [
            'py_file_select=source.command_line:main',
        ],
    },
    setup_requires=['wheel','setuptools']
)
