#!/bin/bash
# Installation script for Sider AI automation

echo "🚀 Setting up Sider AI automation environment..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "myenv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv myenv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source myenv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install packages with retry logic
echo "📥 Installing packages..."
for attempt in 1 2 3; do
    echo "Attempt $attempt/3"
    if pip install selenium webdriver-manager pyautogui --timeout 300; then
        break
    elif [ $attempt -eq 3 ]; then
        echo "❌ Failed to install packages after 3 attempts"
        echo "💡 Try running: pip install -r requirements_minimal.txt"
        exit 1
    else
        echo "⏱️ Retrying in 10 seconds..."
        sleep 10
    fi
done

echo "✅ Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit list_account.txt with your accounts"
echo "2. Run test.py to get coordinates for your screen"
echo "3. Update coordinates in config.py"
echo "4. Run: python main.py"
echo ""
echo "🔍 To test structure: python structure_test.py"