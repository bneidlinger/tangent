#!/usr/bin/env python3
"""
Direct test of the model on the Pi
Tests different connection methods to find what works
"""

import paramiko
import subprocess
import sys

PI_HOST = "192.168.1.31"
PI_USER = "brand"

print("🧪 Testing Tangnet Model Connection\n")

# Method 1: Direct SSH command (requires SSH keys)
print("Method 1: Direct SSH command")
print("-" * 50)
try:
    cmd = f'ssh {PI_USER}@{PI_HOST} "echo Connection test successful"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
    
    if result.returncode == 0:
        print("✓ SSH connection works!")
        
        # Test tangnet alias
        print("\nTesting 'tangnet' command...")
        cmd = f'ssh {PI_USER}@{PI_HOST} "tangnet \\"Hello, can you hear me?\\""'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout:
            print(f"✓ Tangnet works! Response: {result.stdout[:100]}...")
        else:
            print(f"✗ Tangnet failed: {result.stderr}")
            
            # Try direct llama.cpp path
            print("\nTrying direct llama.cpp path...")
            cmd = f'ssh {PI_USER}@{PI_HOST} "cd /home/brand && ./llama.cpp/llama-cli -m models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -c 512 -t 2 -n 50 --no-display-prompt -p \\"Hello\\""'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout:
                print(f"✓ Direct path works! Response: {result.stdout[:100]}...")
            else:
                print(f"✗ Direct path failed: {result.stderr}")
    else:
        print(f"✗ SSH failed: {result.stderr}")
        print("\nTo fix: ssh-copy-id brand@192.168.1.31")
        
except Exception as e:
    print(f"✗ Error: {e}")

# Method 2: Paramiko (can use password)
print("\n\nMethod 2: Paramiko SSH library")
print("-" * 50)
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Try connecting
    try:
        client.connect(PI_HOST, username=PI_USER, timeout=10)
        print("✓ Connected via SSH key")
    except:
        # If you need password auth, uncomment and set password:
        # PASSWORD = "your_password_here"
        # client.connect(PI_HOST, username=PI_USER, password=PASSWORD, timeout=10)
        print("✗ SSH key auth failed. Set password in script if needed.")
        raise
    
    # Test commands
    print("\nFinding llama.cpp...")
    stdin, stdout, stderr = client.exec_command("find ~ -name llama-cli -type f 2>/dev/null | head -5")
    paths = stdout.read().decode().strip().split('\n')
    
    if paths and paths[0]:
        print(f"✓ Found llama-cli at: {paths[0]}")
    
    print("\nFinding model files...")
    stdin, stdout, stderr = client.exec_command("find ~ -name '*.gguf' -type f 2>/dev/null | head -5")
    models = stdout.read().decode().strip().split('\n')
    
    if models and models[0]:
        print(f"✓ Found model at: {models[0]}")
    
    print("\nTesting tangnet alias...")
    stdin, stdout, stderr = client.exec_command("tangnet 'Hello from Paramiko'")
    response = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    
    if response:
        print(f"✓ Tangnet works! Response: {response[:100]}...")
    else:
        print(f"✗ Tangnet failed: {error}")
        
        # Show what might work
        print("\nChecking .bashrc for tangnet definition...")
        stdin, stdout, stderr = client.exec_command("grep -A2 -B2 tangnet ~/.bashrc")
        bashrc_content = stdout.read().decode().strip()
        if bashrc_content:
            print(f"Found in .bashrc:\n{bashrc_content}")
    
    client.close()
    
except Exception as e:
    print(f"✗ Paramiko error: {e}")

print("\n" + "=" * 50)
print("Test complete. Use the working method in your chat app.")