#!/usr/bin/env python3
"""
Simple health check endpoint for Railway deployment
"""
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def health_check():
    return {'status': 'healthy', 'service': 'taofu-bot'}

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'taofu-bot'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting health check server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
