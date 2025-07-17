#!/usr/bin/env python3
"""
PyAutoGUI Coordinate Finder
Use this script to find the exact coordinates for clicking buttons on your screen.
"""

import pyautogui
import time

def main():
    """Main function to get mouse coordinates."""
    print("=" * 60)
    print("PyAutoGUI Coordinate Finder")
    print("=" * 60)
    print("\nInstructions:")
    print("1. This script will wait 5 seconds")
    print("2. During that time, move your mouse to the 'Add extension' button")
    print("3. The script will then display the coordinates")
    print("4. Update these coordinates in config.py")
    print("\nStarting in...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Get current mouse position
    x, y = pyautogui.position()
    
    print(f"\n" + "=" * 60)
    print(f"COORDINATES FOUND:")
    print(f"X = {x}")
    print(f"Y = {y}")
    print("=" * 60)
    
    print(f"\nUpdate your config.py file with:")
    print(f"ADD_EXTENSION_BUTTON_X = {x}")
    print(f"ADD_EXTENSION_BUTTON_Y = {y}")
    
    print(f"\nScreen resolution: {pyautogui.size()}")
    print("\nPress any key to exit...")
    input()

if __name__ == "__main__":
    main()