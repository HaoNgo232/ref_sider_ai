# Sider AI Registration Automation Script

This script automates the registration process for Sider AI accounts and Chrome extension installation.

## Features

- Automated account registration with referral links
- Google OAuth integration
- Chrome extension installation
- Multiple account processing
- Comprehensive logging
- Configurable settings
- Error handling and recovery

## Requirements

- Python 3.7+
- Chrome browser installed
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HaoNgo232/ref_sider_ai.git
cd ref_sider_ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup

1. **Configure account list**: Edit `list_account.txt` with your accounts in the format:
```
email1@example.com|password1
email2@example.com|password2
```

2. **Configure PyAutoGUI coordinates**: 
   - Run `test.py` to find the correct coordinates for the "Add extension" button on your screen
   - Update the coordinates in `config.py`:
```python
ADD_EXTENSION_BUTTON_X = YOUR_X_COORDINATE
ADD_EXTENSION_BUTTON_Y = YOUR_Y_COORDINATE
```

3. **Adjust settings** (optional): Modify `config.py` to customize:
   - Browser window size
   - Wait times
   - URLs
   - Delays between accounts

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Process each account from `list_account.txt`
2. Navigate to Sider AI registration page
3. Click "Register Now & Claim Rewards"
4. Use "Continue with Google" for authentication
5. Complete Google login process
6. Install the Chrome extension
7. Log all activities to `sider_automation.log`

## Files

- `main.py` - Main automation script
- `config.py` - Configuration settings
- `test.py` - Utility to find PyAutoGUI coordinates
- `requirements.txt` - Python dependencies
- `list_account.txt` - Account credentials (email|password format)
- `sider_automation.log` - Log file (created automatically)

## Configuration Options

Edit `config.py` to customize:

```python
# Browser settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DEFAULT_WAIT_TIME = 60
ACCOUNT_DELAY = 30  # Seconds between accounts

# PyAutoGUI coordinates (adjust for your screen)
ADD_EXTENSION_BUTTON_X = 784
ADD_EXTENSION_BUTTON_Y = 270
```

## Troubleshooting

1. **Extension button coordinates not working**: 
   - Run `test.py` and move your mouse to the "Add extension" button
   - Update coordinates in `config.py`

2. **Login failures**:
   - Check account credentials in `list_account.txt`
   - Verify Google accounts don't have 2FA enabled
   - Check logs in `sider_automation.log`

3. **Element not found errors**:
   - Website structure may have changed
   - Check console logs for detailed error messages
   - Update selectors in the code if needed

## Logging

The script creates detailed logs in `sider_automation.log` including:
- Successful registrations
- Error details
- Timing information
- Browser interactions

## Safety Features

- Individual temporary browser profiles for each account
- Proper cleanup of temporary files
- Error handling and recovery
- Rate limiting between accounts

## Legal Notice

This script is for educational purposes. Ensure you comply with:
- Sider AI Terms of Service
- Google Terms of Service
- Applicable laws and regulations

Use responsibly and at your own risk.