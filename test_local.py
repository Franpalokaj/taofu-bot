#!/usr/bin/env python3
"""
Local test script for Taofu bot components
Tests the core functionality without requiring all API keys
"""

import os
import json
from datetime import datetime

def test_knowledge_base():
    """Test knowledge base loading"""
    print("📚 Testing knowledge base...")
    try:
        with open('knowledge.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ Knowledge base loaded ({len(content)} characters)")
        print(f"   Contains {content.count('===')} sections")
        return True
    except FileNotFoundError:
        print("❌ knowledge.txt not found")
        return False
    except Exception as e:
        print(f"❌ Error loading knowledge base: {e}")
        return False

def test_system_instructions():
    """Test system instructions loading"""
    print("⚙️  Testing system instructions...")
    try:
        with open('system_instructions.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ System instructions loaded ({len(content)} characters)")
        print(f"   Contains {content.count('===')} sections")
        return True
    except FileNotFoundError:
        print("❌ system_instructions.txt not found")
        return False
    except Exception as e:
        print(f"❌ Error loading system instructions: {e}")
        return False

def test_analytics_logging():
    """Test analytics logging functionality"""
    print("\n📊 Testing analytics logging...")
    try:
        # Test logging function
        test_data = {
            'timestamp': datetime.now().isoformat(),
            'user_id': 'test_user_123',
            'username': 'test_user',
            'question': 'What is Taofu?',
            'response_preview': 'Taofu is a decentralized ecosystem...',
            'platform': 'Test'
        }
        
        # Load existing analytics or create new
        try:
            with open('analytics.json', 'r') as f:
                analytics = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            analytics = []
        
        # Add test data
        analytics.append(test_data)
        
        # Save back
        with open('analytics.json', 'w') as f:
            json.dump(analytics, f, indent=2)
        
        print("✅ Analytics logging works")
        return True
    except Exception as e:
        print(f"❌ Error testing analytics: {e}")
        return False

def test_environment_setup():
    """Test environment variable setup"""
    print("\n🔧 Testing environment setup...")
    
    # Check if .env exists
    if os.path.exists('.env'):
        print("✅ .env file exists")
    else:
        print("⚠️  .env file not found (create from env.example)")
    
    # Check env.example
    if os.path.exists('env.example'):
        print("✅ env.example exists")
    else:
        print("❌ env.example not found")
        return False
    
    return True

def test_dependencies():
    """Test if required packages can be imported"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'discord',
        'openai', 
        'tweepy',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - run: pip install -r requirements.txt")
            missing.append(package)
    
    return len(missing) == 0

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'bot.py',
        'twitter_bot.py', 
        'knowledge.txt',
        'system_instructions.txt',
        'requirements.txt',
        'railway.json',
        'README.md'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing.append(file)
    
    return len(missing) == 0

def main():
    """Run all tests"""
    print("🧪 Taofu Bot Local Test Suite")
    print("=" * 40)
    
    tests = [
        test_file_structure,
        test_dependencies,
        test_environment_setup,
        test_knowledge_base,
        test_system_instructions,
        test_analytics_logging
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your bot is ready for deployment.")
        print("\nNext steps:")
        print("1. Set up your API keys in .env file")
        print("2. Test locally: python bot.py")
        print("3. Deploy: ./deploy.sh")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Create .env from env.example")
        print("- Check that all files are present")

if __name__ == "__main__":
    main() 