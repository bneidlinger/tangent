@echo off
echo Testing direct llama command...
echo.

echo Running with a simple prompt:
ssh brand@192.168.1.31 "/home/brand/tangnet/llama.cpp/build/bin/llama-cli -m /home/brand/tangnet/llama.cpp/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -c 2048 -t 4 -ngl 33 --no-display-prompt -p \"Hello, how are you?\""

pause