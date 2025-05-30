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
        self.tree_chars = ['├──', '└──', '│', '─']
        
    def parse_tree_line(self, line):
        """Parse a single line from tree output"""
        # Remove tree characters and get indentation level
        original_line = line
        clean_line = line
        
        # Remove common tree characters
        for char in ['├──', '└──', '├── ', '└── ', '│   ', '    ']:
            clean_line = clean_line.replace(char, '')
        
        # Calculate indentation level
        indent_level = 0
        for char in original_line:
            if char in ' │├└─':
                if char == '│':
                    indent_level += 1
                elif char in '├└':
                    break
            else:
                break
        
        # Clean the filename
        filename = clean_line.strip()
        
        # Remove trailing / for directories
        is_directory = filename.endswith('/')
        if is_directory:
            filename = filename.rstrip('/')
            
        return indent_level, filename, is_directory
    
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
        
        for line in lines:
            if not line.strip():
                continue
                
            # Skip the root directory line if it exists
            if '/' in line and line.count('/') == 1 and line.strip().endswith('/'):
                root_name = line.strip().rstrip('/')
                # Update the target path to include root directory name
                if not target_path.name == root_name:
                    target_path = target_path / root_name
                    path_stack = [target_path]
                continue
            
            indent_level, filename, is_directory = self.parse_tree_line(line)
            
            if not filename:
                continue
            
            # Adjust path stack based on indentation
            while len(path_stack) > indent_level + 1:
                path_stack.pop()
            
            # Create the full path
            current_path = path_stack[-1] / filename
            
            try:
                if is_directory:
                    current_path.mkdir(parents=True, exist_ok=True)
                    path_stack.append(current_path)
                    print(f"Created directory: {current_path.relative_to(target_path.parent)}")
                else:
                    # Ensure parent directory exists
                    current_path.parent.mkdir(parents=True, exist_ok=True)
                    # Create empty file
                    current_path.touch()
                    print(f"Created file: {current_path.relative_to(target_path.parent)}")
                    
            except Exception as e:
                print(f"Error creating {current_path}: {e}")
                continue
    
    def run(self, tree_file=None, target_path=None):
        """Main execution function"""
        # Default values
        if tree_file is None:
            tree_file = '.tree'
        if target_path is None:
            target_path = '.'
            
        # Validate tree file
        if not os.path.exists(tree_file):
            print(f"Error: Tree file '{tree_file}' not found.")
            print("Create a .tree file with your directory structure or specify a different file with -f")
            sys.exit(1)
        
        # Read and parse tree file
        lines = self.read_tree_file(tree_file)
        
        # Build structure
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
    
    # Create and run reverse tree
    reverse_tree = ReverseTree()
    reverse_tree.run(tree_file=args.file, target_path=args.source)

if __name__ == '__main__':
    main()