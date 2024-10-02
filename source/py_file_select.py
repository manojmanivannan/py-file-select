#!/usr/bin/env python3

import os
import sys
import subprocess
from time import sleep
import inquirer
import click
from inquirer.themes import GreenPassion

OKGREEN = '\033[32m'
WARNING = '\033[33m'
FAIL    = '\033[31m'
ENDC    = '\033[0m'


def run_find(regex, location, respect_gitignore=True):
    """
    Mimics the behavior of the 'f' function from Bash, respecting .gitignore if present.
    """
    location = os.path.realpath(location)
    
    # Find command
    if respect_gitignore:
        cmd = ['fdfind', '--type','f', regex, location]
    else:
        cmd = ['fdfind', '-I','--type','f', regex, location]

    # Run find command
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        files = result.stdout.strip().splitlines()
        
    except FileNotFoundError:
        # Handle case where 'fdfind' is not found
        print(FAIL + "Error: 'fdfind' command not found." + ENDC)
        print(WARNING + "Please install it using: " + ENDC + OKGREEN + "apt install fd-find" + ENDC)
        sys.exit(1)

    return files

def get_common_path(files):
    """
    Extract the common path from the list of file paths
    """
    return os.path.commonpath(files)


def relative_paths(common_path, files):
    """
    Return relative paths by removing the common path prefix from each file
    """
    return [os.path.relpath(file, common_path) for file in files]


def interactive_file_selection(common_path, relative_files):
    """
    Show the file list interactively and allow the user to select one file
    """
    questions = [
        inquirer.List('file', message="Which file?", choices=relative_files)
    ]
    answers = inquirer.prompt(questions, theme=GreenPassion())
    
    if answers:
        chosen_file = answers["file"]
        full_file_path = os.path.join(common_path, chosen_file)
        print(f"Opening: {full_file_path}")
        sleep(0.5)
        subprocess.run(['vim', full_file_path])


def list_files(result):
    """
    Print the full paths of the matching files
    """
    # print(OKGREEN + "Matched Files:" + ENDC)
    for file in result:
        print(file)

def usage():
    """
    Print usage information for the script
    """
    print(OKGREEN + "Usage: " + ENDC + "py_file_select [--list-only] [--include-gitignore] <REGEX> <LOCATION>")
    print(OKGREEN + "Options:" + ENDC)
    print(WARNING + "  --list-only        " + ENDC + ": Lists all matching files with full paths without opening them.")
    print(WARNING + "  --include-gitignore" + ENDC + ": Include files ignored by git in the search.")
    print(WARNING + "  REGEX              " + ENDC + ": The pattern to search for in the file names.")
    print(WARNING + "  LOCATION           " + ENDC + ": The directory to search within.")
    print("\n")
    print(OKGREEN + "Example:" + ENDC)
    print("  py_file_select 'main' '/path/to/directory'")
    print("  py_file_select --list-only 'main' '/path/to/directory'")
    
    
@click.command()
@click.option('-l','--list-only', is_flag=True, default=False, help="Lists all matching files with full paths without opening them.")
@click.option('-i', '--include-gitignore', is_flag=True, default=True, help="Include files ignored by git in the search")
@click.argument('regex', type=str,required=True)
@click.argument('location', type=click.Path(exists=True), required=True)
def main(list_only, include_gitignore, regex, location):
    """
    Program to search for files matching a given regex in a given directory/location.
    Either list those files or interactively open them.
    """

    # Run the find command and get the result
    result = run_find(regex, location, respect_gitignore=include_gitignore)
    result_length = len(result)

    if list_only:
        # If --list-only flag is set, just list the files and exit
        if result_length > 0:
            list_files(result)
        else:
            print(f"No files found matching: \"{regex}\"")
        sys.exit(0)

    if result_length == 1 and result[0]:
        print("Opening:", result[0])
        sleep(0.5)
        subprocess.run(['vim', result[0]])
    elif result_length > 1:
        common_path = get_common_path(result)
        relative_files = relative_paths(common_path, result)

        # Display the common path once
        print(OKGREEN + "Common Path: " + ENDC + WARNING + common_path + ENDC)

        # Interactive selection from relative paths
        interactive_file_selection(common_path, relative_files)
    else:
        print(f"No files found matching: \"{regex}\"")


if __name__ == "__main__":
    main()
