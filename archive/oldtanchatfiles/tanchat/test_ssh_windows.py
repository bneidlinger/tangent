"""Test SSH connectivity from Windows to Pi"""
import subprocess
import sys

PI_HOST = "192.168.1.31"
PI_USER = "brand"

print(f"Testing SSH connection to {PI_USER}@{PI_HOST}...")
print("-" * 50)

# Test 1: Basic SSH with timeout
print("Test 1: Basic SSH echo test")
try:
    cmd = ['ssh', '-o', 'ConnectTimeout=5', '-o', 'StrictHostKeyChecking=no', 
           f'{PI_USER}@{PI_HOST}', 'echo "Connection successful"']
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    
    if result.returncode == 0:
        print(f"✓ Success: {result.stdout.strip()}")
    else:
        print(f"✗ Failed: {result.stderr}")
except subprocess.TimeoutExpired:
    print("✗ SSH connection timed out")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "-" * 50)

# Test 2: Check if SSH keys are configured
print("Test 2: SSH key authentication test")
try:
    cmd = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=5', 
           f'{PI_USER}@{PI_HOST}', 'echo "Key auth works"']
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    
    if result.returncode == 0:
        print("✓ SSH keys are properly configured")
    else:
        print("✗ SSH keys not configured - password may be required")
        print("  Run: ssh-copy-id brand@192.168.1.31")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "-" * 50)

# Test 3: Test llama.cpp installation
print("Test 3: Testing llama.cpp on Pi")
try:
    cmd = ['ssh', '-o', 'ConnectTimeout=5', f'{PI_USER}@{PI_HOST}', 
           'ls -la /home/brand/tangnet/llama.cpp/build/bin/llama-cli']
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    
    if result.returncode == 0:
        print(f"✓ llama-cli found: {result.stdout.strip()}")
    else:
        print("✗ llama-cli not found at expected path")
        print("  Checking alternate locations...")
        
        # Try alternate path
        cmd2 = ['ssh', '-o', 'ConnectTimeout=5', f'{PI_USER}@{PI_HOST}', 
                'find /home/brand -name "llama-cli" -type f 2>/dev/null | head -1']
        result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=10)
        
        if result2.returncode == 0 and result2.stdout.strip():
            print(f"  Found at: {result2.stdout.strip()}")
        else:
            print("  Could not locate llama-cli")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "-" * 50)
print("If all tests pass, the streaming server should work.")
print("If SSH key auth fails, run: ssh-copy-id brand@192.168.1.31")