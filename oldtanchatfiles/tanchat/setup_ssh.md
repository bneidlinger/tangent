# Setting up SSH for Tangnet Chat

To use the Tangnet Chat server, you need passwordless SSH access to your Raspberry Pi.

## Quick Setup

1. **Generate SSH key (if you don't have one):**
   ```powershell
   ssh-keygen -t rsa -b 4096
   ```
   Just press Enter for all prompts to use defaults.

2. **Copy your SSH key to the Pi:**
   ```powershell
   type $env:USERPROFILE\.ssh\id_rsa.pub | ssh brand@192.168.1.31 "cat >> ~/.ssh/authorized_keys"
   ```
   Enter your Pi password when prompted.

3. **Test the connection:**
   ```powershell
   ssh brand@192.168.1.31 "echo 'SSH works!'"
   ```
   This should print "SSH works!" without asking for a password.

## Running the Chat Server

Once SSH is configured:

```powershell
# Install minimal requirements
pip install fastapi uvicorn aiofiles

# Run the server
python tangnet_chat.py
```

Then open http://localhost:8000 in your browser.

## Troubleshooting

- If SSH asks for a password, the key setup didn't work correctly
- Make sure the Pi's IP is correct (192.168.1.31)
- Ensure the tangnet alias works on the Pi by testing:
  ```bash
  ssh brand@192.168.1.31 "tangnet 'Hello world'"
  ```