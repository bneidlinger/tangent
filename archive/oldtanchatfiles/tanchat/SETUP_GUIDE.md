# Tangnet Chat Setup Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure SSH access to your Pi:**
   ```bash
   ssh-copy-id brand@192.168.1.31
   ```
   
   Or if using password, edit `PI_PASSWORD` in `tangnet_simple_chat.py`

3. **Test the connection:**
   ```bash
   python test_model_direct.py
   ```

4. **Run the chat server:**
   ```bash
   python tangnet_simple_chat.py
   ```

5. **Open your browser:**
   - Go to http://localhost:8000/static/simple.html
   - Start chatting with TinyLlama!

## Troubleshooting

### SSH Connection Failed
- Make sure your Pi is on and connected to network
- Try: `ping 192.168.1.31`
- Set up SSH keys: `ssh-copy-id brand@192.168.1.31`
- Or add your password to the script

### Model Not Responding
- SSH into Pi: `ssh brand@192.168.1.31`
- Test tangnet: `tangnet "Hello"`
- Check model path: `ls ~/models/`

### WebSocket Connection Issues
- Check if server is running
- Try refreshing the page
- Check browser console for errors

## Architecture

This is a minimal implementation with:
- Single Python file (`tangnet_simple_chat.py`)
- Simple HTML interface (`static/simple.html`)
- Direct SSH connection to Pi using Paramiko
- WebSocket for real-time chat
- No database, no complex abstractions

Perfect for chatting with your TinyLlama on the Pi!