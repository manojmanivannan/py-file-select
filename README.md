# PY-FILE-SELECT

This is a tool that allows you to search, list and/or open files in a directory using an interactive selection from the command line.

## Installation

Install via `pipx`:

```bash
pipx install git+https://github.com/manojmanivannan/py-file-select.git
```

## Usage
```bash
Usage: py_file_select [OPTIONS] REGEX LOCATION

  Program to search for files matching a given regex in a given
  directory/location. Either list those files or interactively open them.

Options:
  -l, --list-only          Lists all matching files with full paths without
                           opening them.
  -i, --include-gitignore  Include files ignored by git in the search
  --help                   Show this message and exit.
```