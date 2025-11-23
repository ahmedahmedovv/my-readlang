#!/usr/bin/env python3
"""
Local development server script.
Runs the app on your local network so you can test on multiple devices.
"""
import os
import socket
from app import app

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        # Connect to a remote address (doesn't actually connect)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.getenv('PORT', 8080))
    
    # Get local IP address
    local_ip = get_local_ip()
    
    # Check if API key is set
    if not os.getenv('MISTRAL_API_KEY'):
        print("⚠️  Warning: MISTRAL_API_KEY not set!")
        print("   Set it with: export MISTRAL_API_KEY='your_key'")
        print()
    
    print("=" * 60)
    print("🚀 Starting Interactive Dictionary - Local Development")
    print("=" * 60)
    print()
    print("📱 Access from this computer:")
    print(f"   http://localhost:{port}")
    print(f"   http://127.0.0.1:{port}")
    print()
    print("📱 Access from other devices (tablet, phone, etc.):")
    print(f"   http://{local_ip}:{port}")
    print()
    print("💡 Make sure:")
    print("   - Your devices are on the same Wi-Fi network")
    print("   - Firewall allows connections on port", port)
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)

