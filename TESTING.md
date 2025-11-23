# Local Testing Guide

This guide shows you how to test the Interactive Dictionary app locally on your computer and tablet without deploying to a server.

## Quick Start

### 1. Set up your environment

```bash
# Navigate to project directory
cd /path/to/your/project

# Activate virtual environment (if you have one)
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Set your API key
export MISTRAL_API_KEY="your_api_key_here"
```

### 2. Run the local server

**Option A: Using the helper script (Recommended)**
```bash
python run_local.py
```

**Option B: Using Flask directly**
```bash
export FLASK_DEBUG=True
python app.py
```

**Option C: Using Flask command**
```bash
export FLASK_APP=app.py
export FLASK_DEBUG=True
export MISTRAL_API_KEY="your_api_key_here"
flask run --host=0.0.0.0 --port=8080
```

### 3. Access from your devices

**On your computer:**
- Open browser and go to: `http://localhost:8080`
- Or: `http://127.0.0.1:8080`

**On your tablet/phone (same Wi-Fi network):**
- Open browser and go to: `http://YOUR_COMPUTER_IP:8080`
- The script will show your IP address when you run it
- Example: `http://192.168.1.100:8080`

## Finding Your Computer's IP Address

### macOS/Linux:
```bash
# Method 1: Using the script
python run_local.py  # Shows IP automatically

# Method 2: Using ifconfig
ifconfig | grep "inet " | grep -v 127.0.0.1

# Method 3: Using ip command (Linux)
ip addr show | grep "inet " | grep -v 127.0.0.1
```

### Windows:
```bash
# Method 1: Using ipconfig
ipconfig | findstr IPv4

# Method 2: Look for the IP under your Wi-Fi adapter
ipconfig
```

## Troubleshooting

### Can't access from tablet

**1. Check firewall settings:**

**macOS:**
- System Settings → Network → Firewall
- Allow incoming connections for Python
- Or temporarily disable firewall for testing

**Windows:**
- Windows Defender Firewall → Allow an app through firewall
- Add Python to allowed apps
- Or temporarily disable firewall for testing

**2. Check network connection:**
- Make sure both devices are on the same Wi-Fi network
- Try pinging your computer's IP from the tablet:
  ```
  ping YOUR_COMPUTER_IP
  ```

**3. Check port availability:**
- Make sure no other app is using port 8080
- Change port if needed:
  ```bash
  PORT=5000 python run_local.py
  ```

### Server won't start

**Check if port is in use:**
```bash
# macOS/Linux
lsof -i :8080

# Windows
netstat -ano | findstr :8080
```

**Use a different port:**
```bash
PORT=5000 python run_local.py
```

### API key not working

**Check if it's set:**
```bash
echo $MISTRAL_API_KEY
```

**Set it for current session:**
```bash
export MISTRAL_API_KEY="your_key_here"
```

**Set it permanently (macOS/Linux):**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export MISTRAL_API_KEY="your_key_here"
```

## Development Tips

### Hot Reload
The app runs in debug mode, so changes to Python files will automatically restart the server. Just refresh your browser!

### Clear Cache
If you see old content:
- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Clear browser cache
- Restart the server

### Test on Multiple Devices
1. Start the server on your computer
2. Find your computer's IP address
3. Connect tablet/phone to same Wi-Fi
4. Open browser on tablet and navigate to `http://YOUR_IP:8080`
5. Test the app on both devices simultaneously!

### Mobile Testing
- Use Chrome DevTools on desktop (F12 → Toggle device toolbar)
- Or test on real device for better results
- The app is optimized for iPhone 13 Mini and iPad Mini

## Testing Checklist

- [ ] App loads on computer
- [ ] App loads on tablet/phone
- [ ] Word selection works
- [ ] Translations appear
- [ ] Batch processing works
- [ ] Pagination works (for long texts)
- [ ] Import/export works
- [ ] Page state persists on refresh
- [ ] Selected words persist on refresh
- [ ] Touch interactions work on mobile

## Performance Testing

### Large Files
1. Import a large markdown file (like `little.txt`)
2. Test pagination
3. Test word selection across pages
4. Verify state persistence

### Network Speed
- Test on slow network (use browser DevTools throttling)
- Check loading times
- Verify caching works

## Debugging

### Enable Verbose Logging
Edit `app.py` to change log level:
```python
logging.basicConfig(level=logging.DEBUG)  # More verbose
```

### Browser Console
- Open DevTools (F12)
- Check Console for JavaScript errors
- Check Network tab for API calls

### Server Logs
- Check terminal where server is running
- Look for error messages
- Check API response times

## Quick Test Script

Save this as `quick_test.sh`:

```bash
#!/bin/bash
echo "Starting test server..."
export MISTRAL_API_KEY="your_key_here"
python run_local.py
```

Make it executable:
```bash
chmod +x quick_test.sh
./quick_test.sh
```

## Next Steps

Once testing is complete locally:
1. Commit your changes
2. Push to GitHub
3. Deploy to Render (see DEPLOY.md)

