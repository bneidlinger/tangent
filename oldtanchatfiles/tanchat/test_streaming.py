"""Test streaming output from llama.cpp"""
import subprocess
import sys

PI_HOST = "192.168.1.31"
PI_USER = "brand"

# Test command
llama_path = "/home/brand/tangnet/llama.cpp/build/bin/llama-cli"
model_path = "/home/brand/tangnet/llama.cpp/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

prompt = "Tell me a joke"
cmd = f"ssh {PI_USER}@{PI_HOST} '{llama_path} -m {model_path} -c 512 -t 4 -n 50 --simple-io -p \"{prompt}\"'"

print(f"Running: {cmd}")
print("="*60)
print("Streaming output:")
print("="*60)

# Run with real-time output
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

# Stream output
for line in iter(process.stdout.readline, ''):
    if line:
        sys.stdout.write(line)
        sys.stdout.flush()

# Wait for completion
process.wait()

# Check for errors
if process.returncode != 0:
    print("\nErrors:")
    print(process.stderr.read())

print("\n" + "="*60)
print("Done!")