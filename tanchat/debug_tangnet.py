"""
Debug script to test Tangnet connection
"""

import asyncio
import subprocess

async def test_ssh_connection():
    """Test basic SSH connection"""
    print("Testing SSH connection to Pi...")
    
    cmd = 'ssh brand@192.168.1.31 "echo SSH connection successful"'
    
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            print("✓ SSH connection successful")
            print(f"Output: {stdout.decode().strip()}")
        else:
            print("✗ SSH connection failed")
            print(f"Error: {stderr.decode().strip()}")
            return False
    except Exception as e:
        print(f"✗ SSH connection error: {str(e)}")
        return False
    
    return True

async def test_tangnet_command():
    """Test tangnet command on Pi"""
    print("\nTesting tangnet command...")
    
    cmd = 'ssh brand@192.168.1.31 "tangnet \\"Hello from debug script\\""'
    
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            print("✓ Tangnet command successful")
            print(f"Response: {stdout.decode().strip()}")
        else:
            print("✗ Tangnet command failed")
            print(f"Error: {stderr.decode().strip()}")
            
            # Try alternative command format
            print("\nTrying alternative command format...")
            cmd2 = "ssh brand@192.168.1.31 'tangnet \"Hello from debug script\"'"
            process2 = await asyncio.create_subprocess_shell(
                cmd2,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout2, stderr2 = await process2.communicate()
            
            if process2.returncode == 0:
                print("✓ Alternative format works!")
                print(f"Response: {stdout2.decode().strip()}")
            else:
                print("✗ Alternative format also failed")
                print(f"Error: {stderr2.decode().strip()}")
                
    except Exception as e:
        print(f"✗ Tangnet command error: {str(e)}")

async def test_direct_llama():
    """Test direct llama.cpp command"""
    print("\nTesting direct llama.cpp command...")
    
    cmd = 'ssh brand@192.168.1.31 "./llama.cpp/llama-cli -m models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -c 2048 -t 4 -ngl 33 --no-display-prompt -p \\"Hello from debug\\""'
    
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            print("✓ Direct llama.cpp command successful")
            print(f"Response: {stdout.decode().strip()[:200]}...")  # First 200 chars
        else:
            print("✗ Direct llama.cpp command failed")
            print(f"Error: {stderr.decode().strip()}")
            
    except Exception as e:
        print(f"✗ Direct command error: {str(e)}")

async def main():
    print("=== Tangnet Connection Debug ===\n")
    
    # Test SSH first
    if await test_ssh_connection():
        # Test tangnet command
        await test_tangnet_command()
        
        # Test direct command
        await test_direct_llama()
    else:
        print("\nPlease set up SSH keys first:")
        print("1. Run: ssh-keygen -t rsa -b 4096")
        print("2. Run: type %USERPROFILE%\\.ssh\\id_rsa.pub | ssh brand@192.168.1.31 \"cat >> ~/.ssh/authorized_keys\"")

if __name__ == "__main__":
    asyncio.run(main())