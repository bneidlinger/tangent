@echo off
echo Testing Tangnet paths on Pi...
echo.

echo Checking llama-cli:
ssh brand@192.168.1.31 "ls -la /home/brand/tangnet/llama.cpp/build/bin/llama-cli"
echo.

echo Checking for model files:
ssh brand@192.168.1.31 "find /home/brand -name '*.gguf' | head -5"
echo.

echo Testing llama-cli execution:
ssh brand@192.168.1.31 "/home/brand/tangnet/llama.cpp/build/bin/llama-cli --version"
echo.

pause