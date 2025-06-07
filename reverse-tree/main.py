#!/usr/bin/env python3
"""
reverse-tree - A tool to create directory structures from tree format files

Usage:
    reverse-tree                    # Uses .tree file in current directory
    reverse-tree -f <file>          # Uses specified tree file
    reverse-tree -s <path>          # Sets target directory
    reverse-tree -f <file> -s <path># Uses specified file and target directory
    reverse-tree --help             # Shows help message
    reverse-tree --version          # Shows version
"""

import os
import sys
import argparse
import re
from pathlib import Path

__version__ = "1.0.0"

class ReverseTree:
    def __init__(self):
        self.tree_chars = ["├──", "└──", "│", "─"]
        
    def parse_tree_line(self, line):
        """Parse a single line from tree output"""
        match = re.match(r"^(?:[│ ]*(?:├──|└──) )?([^\n]+)", line)
        if not match:
            return 0, "", False

        filename_part = match.group(1)
        indent_level = 0
        indent_match = re.match(r"^([│ ]*)", line)
        if indent_match:
            indent_str = indent_match.group(1)
            indent_level = indent_str.count("│   ") + indent_str.count("    ")
            if line.strip().startswith("├──") or line.strip().startswith("└──"):
                indent_level += 1

        is_directory = filename_part.endswith("/")
        if is_directory:
            filename = filename_part.rstrip("/")
        else:
            filename = filename_part
            
        return indent_level, filename.strip(), is_directory
    
    def read_tree_file(self, tree_file):
        """Read and parse tree file"""
        try:
            with open(tree_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: Tree file '{tree_file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading tree file: {e}")
            sys.exit(1)
            
        return [line.rstrip('\n\r') for line in lines if line.strip()]
    
    def build_structure(self, lines, target_path):
        """Build directory structure from parsed lines"""
        target_path = Path(target_path).resolve()
        path_stack = [target_path]
        
        print(f"Creating structure in: {target_path}")
        
        actual_root_path = target_path
        first_line_processed = False

        for line in lines:
            if not line.strip():
                continue
                
            indent_level, filename, is_directory = self.parse_tree_line(line)
            
            if not filename:
                continue

            if not first_line_processed:
                if is_directory:
                    actual_root_path = target_path / filename
                    actual_root_path.mkdir(parents=True, exist_ok=True)
                    path_stack = [actual_root_path]
                    print(f"Created directory: {actual_root_path.relative_to(target_path.parent)}")
                else:
                    current_path = target_path / filename
                    current_path.parent.mkdir(parents=True, exist_ok=True)
                    current_path.touch()
                    print(f"Created file: {current_path.relative_to(target_path.parent)}")
                first_line_processed = True
                continue

            while len(path_stack) > indent_level:
                path_stack.pop()
            
            current_path = path_stack[-1] / filename
            
            try:
                if is_directory:
                    current_path.mkdir(parents=True, exist_ok=True)
                    path_stack.append(current_path)
                    print(f"Created directory: {current_path.relative_to(actual_root_path.parent)}")
                else:
                    current_path.parent.mkdir(parents=True, exist_ok=True)
                    current_path.touch()
                    print(f"Created file: {current_path.relative_to(actual_root_path.parent)}")
                    
            except Exception as e:
                print(f"Error creating {current_path}: {e}")
                continue
    
    def run(self, tree_file=None, target_path=None):
        """Main execution function"""
        if tree_file is None:
            tree_file = ".tree"
        if target_path is None:
            target_path = "."
            
        if not os.path.exists(tree_file):
            print(f"Error: Tree file '{tree_file}' not found.")
            print("Create a .tree file with your directory structure or specify a different file with -f")
            sys.exit(1)
        
        lines = self.read_tree_file(tree_file)
        self.build_structure(lines, target_path)
        print(f"\nStructure created successfully from '{tree_file}'")

def main():
    parser = argparse.ArgumentParser(
        description='Create directory structures from tree format files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  reverse-tree                     Create structure from .tree file
  reverse-tree -f project.tree     Use project.tree file
  reverse-tree -s /tmp/project     Create structure in /tmp/project
  reverse-tree -f app.tree -s ~/myapp  Use app.tree and create in ~/myapp

Tree file format:
  project/
  ├── src/
  │   ├── main.py
  │   └── utils.py
  └── README.md
        """
    )
    
    parser.add_argument('-f', '--file', 
                       help='Tree file to read (default: .tree)',
                       default=None)
    
    parser.add_argument('-s', '--source', '--target',
                       help='Target directory to create structure (default: current directory)',
                       default=None)
    
    parser.add_argument('--version', 
                       action='version', 
                       version=f'reverse-tree {__version__}')
    
    args = parser.parse_args()
    reverse_tree = ReverseTree()
    reverse_tree.run(tree_file=args.file, target_path=args.source)

if __name__ == '__main__':
    main()