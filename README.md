# reverse-tree

A command-line tool that creates directory structures from tree-format files. The reverse of the `tree` command - instead of showing directory structure, it creates one!

## Installation

### Ubuntu/Debian (APT):
```bash
sudo add-apt-repository ppa:augustoperin/reverse-tree
sudo apt update
sudo apt install reverse-tree
```

### Other systems (pip):
```bash
pip install reverse-tree
```

### From source:
```bash
git clone https://github.com/AugustoPerin/reverse-tree
cd reverse-tree
pip install .
```

## Usage

### Basic Usage
Create a `.tree` file in your directory with your desired structure:

```
project/
├── src/
│   ├── main.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── config.py
├── tests/
│   ├── test_main.py
│   └── __init__.py
├── README.md
└── requirements.txt
```

Then run:
```bash
reverse-tree
```

### Command Options

```bash
reverse-tree                    # Uses .tree file in current directory
reverse-tree -f myproject.tree  # Uses specified tree file
reverse-tree -s /path/to/target # Creates structure in specified directory
reverse-tree -f app.tree -s ~/projects  # Combines both options
reverse-tree --help             # Shows help message
reverse-tree --version          # Shows version
```

## Examples

### Example 1: Web Application
Create a `webapp.tree` file:
```
webapp/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── views/
│   │   ├── __init__.py
│   │   └── main.py
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
├── tests/
│   └── test_app.py
├── requirements.txt
└── README.md
```

Run: `reverse-tree -f webapp.tree`

### Example 2: Python Package
Create a `package.tree` file:
```
my-package/
├── my_package/
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── setup.py
├── README.md
└── LICENSE
```

Run: `reverse-tree -f package.tree -s ~/projects`

## Tree File Format

The tool supports standard `tree` command output format:

- `├──` (branch)
- `└──` (last branch)  
- `│` (pipe for continuation)
- Spaces for indentation
- `/` at the end of directory names (optional)

## Features

- 🌳 Convert tree-format text into real directory structures
- 📁 Automatically creates directories and empty files
- 🎯 Flexible input and output options
- 🚀 Simple and intuitive command-line interface
- 🐧 Native Linux support with APT installation

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only built-in Python modules)

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## Support

If you encounter any issues:

1. Check existing [issues](https://github.com/AugustoPerin/reverse-tree/issues)
2. Create a new issue with:
   - Your tree file content
   - Command used
   - Expected vs actual result
   - Error messages (if any)

## Related Tools

- `tree` - Display directory tree structures
- `mkdir -p` - Create nested directories
- `find` - Search for files and directories