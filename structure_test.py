#!/usr/bin/env python3
"""
Simple test to verify the script structure without running the full automation.
"""

import sys
import os

def test_structure():
    """Test that all required files exist and have proper structure."""
    print("Testing script structure...")
    
    required_files = [
        'main.py',
        'config.py', 
        'test.py',
        'requirements.txt',
        'list_account.txt',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    
    # Test config import
    try:
        import config
        print("✅ Config module imports successfully")
        
        # Check required config variables
        required_vars = [
            'SIDER_REFERRAL_URL',
            'CHROME_EXTENSION_URL', 
            'WINDOW_WIDTH',
            'WINDOW_HEIGHT',
            'DEFAULT_WAIT_TIME',
            'ADD_EXTENSION_BUTTON_X',
            'ADD_EXTENSION_BUTTON_Y'
        ]
        
        for var in required_vars:
            if not hasattr(config, var):
                print(f"❌ Missing config variable: {var}")
                return False
        
        print("✅ All config variables present")
        
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    # Test account file format
    try:
        with open('list_account.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            
        if not lines:
            print("⚠️  No accounts found in list_account.txt")
        else:
            for i, line in enumerate(lines, 1):
                if '|' not in line:
                    print(f"❌ Invalid format in line {i}: {line}")
                    return False
            print(f"✅ Account file format valid ({len(lines)} accounts)")
            
    except Exception as e:
        print(f"❌ Error reading account file: {e}")
        return False
    
    print("\n🎉 Script structure test passed!")
    return True

if __name__ == "__main__":
    if test_structure():
        sys.exit(0)
    else:
        sys.exit(1)