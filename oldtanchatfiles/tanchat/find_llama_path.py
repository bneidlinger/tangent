#!/usr/bin/env python3
"""
Find the correct llama.cpp paths on the Pi
"""

import paramiko

PI_HOST = "192.168.1.31"
PI_USER = "brand"

print("🔍 Finding llama.cpp installation on Pi...\n")

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(PI_HOST, username=PI_USER, timeout=10)
    
    # Find llama-cli
    print("Searching for llama-cli...")
    stdin, stdout, stderr = client.exec_command("find ~ -name 'llama-cli' -type f 2>/dev/null")
    llama_paths = stdout.read().decode().strip().split('\n')
    
    if llama_paths and llama_paths[0]:
        print(f"✓ Found llama-cli at:")
        for path in llama_paths:
            if path:
                print(f"  {path}")
    
    # Find model files
    print("\nSearching for model files...")
    stdin, stdout, stderr = client.exec_command("find ~ -name '*.gguf' -type f 2>/dev/null")
    model_paths = stdout.read().decode().strip().split('\n')
    
    if model_paths and model_paths[0]:
        print(f"✓ Found models at:")
        for path in model_paths:
            if path:
                print(f"  {path}")
    
    # Check common locations
    print("\nChecking common locations...")
    locations = [
        "/home/brand/llama.cpp/llama-cli",
        "/home/brand/llama.cpp/build/bin/llama-cli",
        "/home/brand/llama.cpp/main",
        "/home/brand/tangnet/llama.cpp/llama-cli",
        "/home/brand/tangnet/llama.cpp/build/bin/llama-cli"
    ]
    
    for loc in locations:
        stdin, stdout, stderr = client.exec_command(f"test -f {loc} && echo 'EXISTS' || echo 'NOT FOUND'")
        result = stdout.read().decode().strip()
        print(f"  {loc}: {result}")
    
    # Check for server binary
    print("\nChecking for server binary...")
    stdin, stdout, stderr = client.exec_command("find ~ -name 'server' -path '*/llama.cpp/*' -type f 2>/dev/null")
    server_paths = stdout.read().decode().strip().split('\n')
    
    if server_paths and server_paths[0]:
        print(f"✓ Found server at:")
        for path in server_paths:
            if path:
                print(f"  {path}")
    
    # Test a direct command
    print("\nTesting direct command...")
    # Try most common path first
    test_cmd = "/home/brand/llama.cpp/llama-cli -v"
    stdin, stdout, stderr = client.exec_command(test_cmd)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    
    if output:
        print(f"✓ Version info: {output}")
    else:
        print(f"✗ Error: {error}")
    
    client.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
    
print("\nUse the paths found above in your chat application!")