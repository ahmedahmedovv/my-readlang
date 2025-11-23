# Quick Start Guide - Local Testing

## 🚀 Fastest Way to Test Locally

### Step 1: Set your API key (one time)
```bash
export MISTRAL_API_KEY="your_api_key_here"
```

### Step 2: Start the server
```bash
# Option 1: Use the helper script (easiest)
python run_local.py

# Option 2: Use the shell script
./start.sh

# Option 3: Direct Flask command
python app.py
```

### Step 3: Access from your devices

**On your computer:**
- Open browser: `http://localhost:8080`

**On your tablet/phone:**
1. Make sure both devices are on the **same Wi-Fi network**
2. The script will show your computer's IP address (e.g., `192.168.1.100`)
3. Open browser on tablet: `http://192.168.1.100:8080`

## 📱 Example

When you run `python run_local.py`, you'll see:
```
🚀 Starting Interactive Dictionary - Local Development
================================================================
📱 Access from this computer:
   http://localhost:8080
   http://127.0.0.1:8080

📱 Access from other devices (tablet, phone, etc.):
   http://192.168.1.100:8080
```

Just use the IP address shown on your tablet!

## ✅ Quick Test

1. **Start server** → `python run_local.py`
2. **Open on computer** → `http://localhost:8080`
3. **Open on tablet** → `http://YOUR_IP:8080` (use IP shown by script)
4. **Select some words** → Test the app!
5. **Refresh** → Page and selections should be remembered!

## 🛠️ Troubleshooting

**Can't access from tablet?**
- Check both devices are on same Wi-Fi
- Check firewall isn't blocking port 8080
- Try a different port: `PORT=5000 python run_local.py`

**Need to find your IP manually?**
```bash
# macOS
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig | findstr IPv4
```

## 📖 More Details

See [TESTING.md](TESTING.md) for comprehensive testing guide.

