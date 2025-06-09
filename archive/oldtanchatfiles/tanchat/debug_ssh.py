#!/usr/bin/env python3
"""Debug script to find correct paths on the Pi"""

import subprocess
import sys

PI_HOST = "192.168.1.31"
PI_USER = "brand"

commands = [
    # Check home directory
    f'ssh {PI_USER}@{PI_HOST} "pwd"',
    
    # List home directory
    f'ssh {PI_USER}@{PI_HOST} "ls -la ~/"',
    
    # Check for llama.cpp in various locations
    f'ssh {PI_USER}@{PI_HOST} "find ~ -name llama-cli -type f 2>/dev/null | head -5"',
    
    # Check for models
    f'ssh {PI_USER}@{PI_HOST} "find ~ -name *.gguf -type f 2>/dev/null | head -5"',
    
    # Check aliases
    f'ssh {PI_USER}@{PI_HOST} "alias | grep tangnet || echo No tangnet alias"',
    
    # Check .bashrc for tangnet
    f'ssh {PI_USER}@{PI_HOST} "grep -n tangnet ~/.bashrc || echo No tangnet in bashrc"',
    
    # Check .bash_aliases
    f'ssh {PI_USER}@{PI_HOST} "cat ~/.bash_aliases 2>/dev/null || echo No .bash_aliases"',
    
    # Check PATH
    f'ssh {PI_USER}@{PI_HOST} "echo PATH=$PATH"',
]

print("Debugging SSH connection to Pi...\n")

for cmd in commands:
    print(f"\n{'='*60}")
    print(f"Running: {cmd}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.stdout:
            print("Output:")
            print(result.stdout)
        if result.stderr:
            print("Error:")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("Command timed out!")
    except Exception as e:
        print(f"Error: {e}")

print("\n\nDone! Use the information above to update tangnet_chat.py")