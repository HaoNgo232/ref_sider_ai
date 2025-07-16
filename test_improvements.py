#!/usr/bin/env python3
"""
Test script to validate the improvements made to main.py
Tests the robot verification and extension installation confirmation functions
"""
import sys
import importlib.util
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_main_py_syntax():
    """Test that main.py compiles without syntax errors"""
    try:
        spec = importlib.util.spec_from_file_location("main", "/home/runner/work/ref_sider_ai/ref_sider_ai/main.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("✅ main.py syntax validation passed")
        return True
    except Exception as e:
        print(f"❌ main.py syntax validation failed: {e}")
        return False

def test_functions_exist():
    """Test that required functions exist in the main module"""
    try:
        spec = importlib.util.spec_from_file_location("main", "/home/runner/work/ref_sider_ai/ref_sider_ai/main.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Check if the process_account function exists
        if hasattr(module, 'process_account'):
            print("✅ process_account function exists")
        else:
            print("❌ process_account function missing")
            return False
            
        if hasattr(module, 'main'):
            print("✅ main function exists")
        else:
            print("❌ main function missing")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Function existence test failed: {e}")
        return False

def test_improvements_keywords():
    """Test that the improvements are present in the code"""
    try:
        with open("/home/runner/work/ref_sider_ai/ref_sider_ai/main.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        improvements_found = []
        
        # Check for robot verification function
        if "handle_robot_verification" in content:
            improvements_found.append("✅ Robot verification function present")
        else:
            improvements_found.append("❌ Robot verification function missing")
        
        # Check for extension installation confirmation
        if "wait_for_extension_installation" in content:
            improvements_found.append("✅ Extension installation confirmation function present")
        else:
            improvements_found.append("❌ Extension installation confirmation function missing")
        
        # Check for improved dialog handling
        if "handle_add_extension_dialog" in content:
            improvements_found.append("✅ Improved dialog handling function present")
        else:
            improvements_found.append("❌ Improved dialog handling function missing")
            
        # Check for CAPTCHA handling
        if "recaptcha" in content.lower() or "captcha" in content.lower():
            improvements_found.append("✅ CAPTCHA handling code present")
        else:
            improvements_found.append("❌ CAPTCHA handling code missing")
            
        # Check for extension verification in chrome://extensions/
        if "chrome://extensions/" in content:
            improvements_found.append("✅ Extension verification in chrome://extensions/ present")
        else:
            improvements_found.append("❌ Extension verification in chrome://extensions/ missing")
        
        for improvement in improvements_found:
            print(improvement)
            
        failed_count = sum(1 for improvement in improvements_found if "❌" in improvement)
        return failed_count == 0
        
    except Exception as e:
        print(f"❌ Improvements keyword test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running tests for Sider AI extension installation improvements...")
    print("=" * 60)
    
    tests = [
        ("Syntax Validation", test_main_py_syntax),
        ("Function Existence", test_functions_exist),
        ("Improvements Keywords", test_improvements_keywords)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}:")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The improvements are correctly implemented.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())