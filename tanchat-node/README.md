# Rick's TinyLlama Portal - Setup Guide

*"Look Morty, I turned a Raspberry Pi into an interdimensional AI portal! It's like having the Council of Ricks in a tiny computer!"*

## Prerequisites

- Raspberry Pi 5 (8GB recommended) with Raspbian OS
- Node.js 18+ installed
- TinyLlama model already set up with llama.cpp
- Network connection

## Installation on Raspberry Pi

1. **SSH into your Pi:**
```bash
ssh brand@192.168.1.31
```

2. **Clone or copy the tanchat-node directory to your Pi:**
```bash
# If using git
git clone <your-repo-url>
cd tangnet/tanchat-node

# Or copy from your local machine
scp -r /mnt/c/projects/tangnet/tanchat-node brand@192.168.1.31:~/
```

3. **Install Node.js (if not already installed):**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

4. **Install dependencies:**
```bash
cd ~/tanchat-node
npm install
```

5. **Configure the model path:**
Edit the `.env` file to match your model location:
```bash
nano .env
# Update MODEL_PATH to your actual path
# Default: MODEL_PATH=/home/brand/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

## Running the Server

1. **Start the server on your Pi:**
```bash
npm start
```

You should see:
```
Loading model from: /home/brand/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
Model loaded successfully!
TanChat Node server running on http://localhost:3000
WebSocket available on ws://localhost:3000
```

2. **Access from your local machine:**
Open your browser and navigate to:
```
http://192.168.1.31:3000
```

## Running as a Service (Optional)

To keep the server running even after SSH disconnects:

1. **Create a systemd service:**
```bash
sudo nano /etc/systemd/system/tanchat.service
```

2. **Add the following content:**
```ini
[Unit]
Description=Rick's TinyLlama Portal
After=network.target

[Service]
Type=simple
User=brand
WorkingDirectory=/home/brand/tanchat-node
ExecStart=/usr/bin/node index.js
Restart=on-failure
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

3. **Enable and start the service:**
```bash
sudo systemctl enable tanchat.service
sudo systemctl start tanchat.service
sudo systemctl status tanchat.service
```

## Troubleshooting

### Model fails to load
- Check that the model path in `.env` is correct
- Ensure the model file exists and is readable
- Verify you have enough RAM (monitor with `htop`)

### Server crashes or runs slowly
- The Pi might be running out of memory
- Try reducing CONTEXT_SIZE in `.env` (default: 2048)
- Reduce GPU_LAYERS if GPU memory is limited

### Can't connect from browser
- Check firewall settings: `sudo ufw allow 3000`
- Verify the Pi's IP address: `hostname -I`
- Ensure the server is running: `sudo systemctl status tanchat`

### WebSocket connection fails
- Clear browser cache and cookies
- Try a different browser
- Check for proxy/VPN interference

## Performance Tips

1. **Use GPU acceleration:**
   - The default config uses 33 GPU layers for Pi 5
   - Adjust GPU_LAYERS in `.env` based on your Pi model

2. **Optimize for your use case:**
   - Reduce CONTEXT_SIZE for faster responses
   - Adjust THREADS based on your Pi's CPU cores

3. **Monitor performance:**
   ```bash
   htop  # Monitor CPU and RAM usage
   vcgencmd measure_temp  # Check temperature
   ```

## Rick's Final Words

*"Listen, this setup is so simple even Jerry could do it. But if you mess it up, don't come crying to me. I'll be in my garage, working on something that actually matters. Like a portal gun for AI models. Peace out!"*

**WUBBA LUBBA DUB DUB!** 🧪🚀