#!/usr/bin/env python3
"""
Start llama.cpp server on the Pi and connect via HTTP API
This is more reliable than SSH command execution
"""

import paramiko
import time
import httpx
import asyncio

PI_HOST = "192.168.1.31"
PI_USER = "brand"

def start_server_on_pi():
    """Start the llama.cpp server on the Pi"""
    print("🚀 Starting llama.cpp server on Pi...")
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(PI_HOST, username=PI_USER, timeout=10)
        
        # Kill any existing server
        print("Stopping any existing server...")
        client.exec_command("pkill -f 'server.*gguf' || true")
        time.sleep(2)
        
        # Find server binary
        stdin, stdout, stderr = client.exec_command(
            "find /home/brand -name 'server' -path '*/llama.cpp/*' -type f 2>/dev/null | head -1"
        )
        server_path = stdout.read().decode().strip()
        
        if not server_path:
            print("❌ Server binary not found!")
            print("You need to build llama.cpp with server support:")
            print("  cd ~/llama.cpp && make clean && make server")
            return False
        
        print(f"✓ Found server at: {server_path}")
        
        # Find model
        stdin, stdout, stderr = client.exec_command(
            "find /home/brand -name 'tinyllama*.gguf' -type f 2>/dev/null | head -1"
        )
        model_path = stdout.read().decode().strip()
        
        if not model_path:
            print("❌ Model not found!")
            return False
            
        print(f"✓ Found model at: {model_path}")
        
        # Start server in background
        server_cmd = f"nohup {server_path} -m {model_path} -t 4 --host 0.0.0.0 --port 8080 -c 2048 > /tmp/llama-server.log 2>&1 &"
        print(f"Starting server...")
        stdin, stdout, stderr = client.exec_command(server_cmd)
        
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(5)
        
        # Check if server is running
        stdin, stdout, stderr = client.exec_command("ps aux | grep -v grep | grep 'server.*gguf'")
        output = stdout.read().decode().strip()
        
        if output:
            print("✓ Server is running!")
            print("\nYou can now access:")
            print(f"  - Web UI: http://{PI_HOST}:8080")
            print(f"  - API: http://{PI_HOST}:8080/v1/chat/completions")
            print("\nTo view logs: ssh {PI_USER}@{PI_HOST} tail -f /tmp/llama-server.log")
            return True
        else:
            print("❌ Server failed to start")
            stdin, stdout, stderr = client.exec_command("tail -20 /tmp/llama-server.log")
            print("Last log entries:")
            print(stdout.read().decode())
            return False
            
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_api():
    """Test the API connection"""
    print("\n🧪 Testing API connection...")
    
    async with httpx.AsyncClient() as client:
        try:
            # Test health endpoint
            response = await client.get(f"http://{PI_HOST}:8080/health", timeout=5.0)
            print(f"✓ Health check: {response.status_code}")
            
            # Test chat completion
            response = await client.post(
                f"http://{PI_HOST}:8080/v1/chat/completions",
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Say hello!"}],
                    "temperature": 0.7,
                    "max_tokens": 50
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Chat API works!")
                print(f"Response: {result['choices'][0]['message']['content']}")
            else:
                print(f"❌ Chat API error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    if start_server_on_pi():
        asyncio.run(test_api())
    else:
        print("\nTroubleshooting:")
        print("1. SSH to Pi: ssh brand@192.168.1.31")
        print("2. Build server: cd ~/llama.cpp && make server")
        print("3. Check model exists: ls ~/models/")
        print("4. Run manually: ./server -m model.gguf --host 0.0.0.0 --port 8080")