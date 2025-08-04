#!/usr/bin/env python3
"""
Startup script for Railway deployment
Runs both Discord bot and health check server
"""
import os
import threading
import subprocess
import sys
from flask import Flask

# Create Flask app for health checks
app = Flask(__name__)

@app.route('/')
def health_check():
    return {'status': 'healthy', 'service': 'taofu-bot'}

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'taofu-bot'}

def run_flask():
    """Run Flask health check server"""
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

def run_discord_bot():
    """Run Discord bot"""
    subprocess.run([sys.executable, 'bot.py'])

if __name__ == '__main__':
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Run Discord bot in main thread
    run_discord_bot()
