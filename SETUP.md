# Setup Instructions - AI Investment Desk Note Generator

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Windows Setup](#windows-setup)
3. [macOS Setup](#macos-setup)
4. [Linux Setup](#linux-setup)
5. [Getting API Key](#getting-anthropic-api-key)
6. [Verification & Testing](#verification--testing)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum
- **Disk Space**: 500MB free space
- **Internet**: Required for LLM API calls

### Recommended
- **RAM**: 8GB or more
- **Modern browser**: Chrome, Firefox, or Safari
- **Antivirus**: Latest definitions

### Check Your Python Version
```bash
python --version
# Should return Python 3.8.0 or higher
```

---

## Windows Setup

### Step 1: Download & Install Python
1. Visit https://www.python.org/downloads/
2. Download **Python 3.11** or higher
3. Run installer
4. ✅ **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"
6. Wait for installation to complete

### Step 2: Verify Python Installation
Open Command Prompt (cmd.exe) and type:
```bash
python --version
pip --version
```

### Step 3: Clone/Download Project
- Download the project folder to your desired location
- Or use Git (if installed):
```bash
git clone <repository-url>
cd AI-Investment-Desk-Generator
```

### Step 4: Create Virtual Environment
```bash
# Navigate to project directory
cd C:\path\to\AI-Investment-Desk-Generator

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```
You should see `(venv)` prefix in your terminal.

### Step 5: Update pip and Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all packages
pip install -r requirements.txt
```

This will install:
- streamlit
- pandas
- plotly
- anthropic
- reportlab
- openpyxl
- python-dotenv

**Expected time**: 2-5 minutes

### Step 6: Verify Installation
```bash
# Check if Streamlit is installed
streamlit --version

# Should output: Streamlit, version X.XX.X
```

### Step 7: Run the Application
```bash
streamlit run app.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Step 8: Access in Browser
- Automatically opens or visit: `http://localhost:8501`
- You should see the AI Investment Desk Note Generator interface

---

## macOS Setup

### Step 1: Install Python
Using Homebrew (recommended):
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

Or download from https://www.python.org/downloads/

### Step 2: Verify Installation
```bash
python3 --version
pip3 --version
```

### Step 3: Download Project
```bash
git clone <repository-url>
cd AI-Investment-Desk-Generator
```

Or manually download and extract the folder.

### Step 4: Create Virtual Environment
```bash
python3 -m venv venv

# Activate
source venv/bin/activate
```

You should see `(venv)` prefix in terminals.

### Step 5: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Run Application
```bash
streamlit run app.py
```

### Step 7: Access in Browser
Visit: `http://localhost:8501`

### For M1/M2 Macs (Apple Silicon)
If you encounter issues, the dependencies are compatible:
```bash
# They will automatically install ARM64 versions
pip install -r requirements.txt
```

---

## Linux Setup

### Ubuntu/Debian:

```bash
# Update package manager
sudo apt update
sudo apt upgrade

# Install Python and pip
sudo apt install python3.11 python3.11-venv python3-pip

# Verify
python3 --version
```

### Download Project
```bash
git clone <repository-url>
cd AI-Investment-Desk-Generator
```

### Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Run Application
```bash
streamlit run app.py
```

### Run in Background (using screen)
```bash
# Start new screen session
screen -S app_session

# Run app
streamlit run app.py

# Detach: Ctrl+A, then D
# Reattach: screen -r app_session
```

---

## Getting Google Gemini API Key (FREE)

### Step-by-Step Guide

1. **Visit Google AI Studio**: https://ai.google.dev/

2. **Sign In**:
   - Use your Google account
   - If no account, create one (free)

3. **Navigate to API Keys**:
   - Click on "Get API Key"
   - Or go directly to: https://ai.google.dev/tutorials#rest_quickstart

4. **Create New API Key**:
   - Click "Create API Key" button
   - Select a project or create new
   - Copy the key immediately

5. **Copy Your Key**:
   - ✅ Key is generated instantly
   - Copy and save securely
   - Keep it private (don't share or commit to GitHub)

6. **Testing the Key**:
   ```python
   import google.generativeai as genai
   
   api_key = "your_key_here"
   genai.configure(api_key=api_key)
   model = genai.GenerativeModel('gemini-pro')
   
   response = model.generate_content("Hello!")
   print(response.text)
   ```

### Using the API Key in the App

**Option 1: Enter in Streamlit Interface** (Easiest)
1. Run: `streamlit run app.py`
2. Go to sidebar → "LLM Configuration"
3. Paste your API key in "Enter Google Gemini API Key"

**Option 2: Use Environment Variable**
```bash
# Windows (Command Prompt)
set GOOGLE_API_KEY=your_key_here

# Windows (PowerShell)
$env:GOOGLE_API_KEY = "your_key_here"

# macOS/Linux (Bash)
export GOOGLE_API_KEY="your_key_here"
```

**Option 3: Use .env File**
```bash
# Create .env file in project root
# (Add to .gitignore before committing!)
echo GOOGLE_API_KEY=your_key_here > .env
```

---

## Verification & Testing

### Test 1: Check Installations
```bash
# Activate venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Test each package
python -c "import streamlit; print('✓ Streamlit OK')"
python -c "import pandas; print('✓ Pandas OK')"
python -c "import plotly; print('✓ Plotly OK')"
python -c "import anthropic; print('✓ Anthropic OK')"
python -c "import reportlab; print('✓ ReportLab OK')"
```

### Test 2: Run Sample Analysis
1. Start app: `streamlit run app.py`
2. In left sidebar, paste your API key
3. Select "Quick Sample Analysis" mode
4. Choose "Tata Motors" from dropdown
5. Click "Generate Desk Note"
6. Wait 30-60 seconds
7. Should display full professional report

### Test 3: Test Download Feature
1. Generate a report (see Test 2)
2. Scroll down to "Download Report" section
3. Click "Download as TXT"
4. Verify file downloads to your computer

### Test 4: Test Data Upload
1. From Tab 1, choose "Upload CSV/Excel"
2. Use sample file or create own with format:
   ```
   Year,Revenue_Cr,EBITDA_Cr,Net_Profit_Cr,Operating_Margin_%,Net_Margin_%,ROE_%,ROA_%,Debt_Equity_Ratio,Market_Cap_Cr,PE_Ratio
   2021,100000,20000,10000,20,10,15,8,0.5,500000,35
   ```
3. Upload and generate report

---

## Troubleshooting

### Problem: "python: command not found"
**Windows**:
- Reinstall Python and check "Add Python to PATH"
- Use `python.exe` instead of `python`

**macOS/Linux**:
```bash
# Use python3 instead
python3 --version

# Or create alias
alias python=python3
```

### Problem: "pip install" fails
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then try:
pip install -r requirements.txt

# If still fails, install one by one:
pip install streamlit
pip install pandas
pip install plotly
# ... etc
```

### Problem: "module not found" error
```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

### Problem: Port 8501 already in use
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

### Problem: API Key showing errors
1. Verify key is correct (copy from Anthropic console)
2. Check key hasn't been revoked
3. Ensure key has API credits (free tier gets some)
4. Try creating new key

### Problem: "FileNotFoundError: sample_financials.csv"
Make sure you have the correct folder structure:
```
AI-Investment-Desk-Generator/
├── app.py
├── requirements.txt
├── data/
│   └── sample_financials.csv  ← Verify this exists
└── utils/
```

### Problem: LLM API rate limited
- Free tier has usage limits
- Wait a few minutes before next request
- Consider upgrading Anthropic account

### Problem: Slow performance
- LLM calls naturally take 30-60 seconds
- Check internet connection
- Try on same network (not VPN if possible)

---

## Next Steps After Setup

1. **Generate First Report**
   - Use Quick Sample mode
   - Choose a company from the list
   - Click "Generate Desk Note"

2. **Explore Data Tab**
   - View sample financial data
   - Filter by sector
   - Understand data structure

3. **Read Documentation**
   - Click "About" tab
   - Review README.md
   - Explore module files

4. **Upload Custom Data**
   - Prepare your CSV with financial data
   - Upload and generate custom report

5. **Download & Share**
   - Export reports as PDF/TXT
   - Share with classmates/teammates

---

## Quick Reference

### Commands to Remember

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Run the application
streamlit run app.py

# Install dependencies
pip install -r requirements.txt

# Check versions
Python --version
pip --version
streamlit --version
```

### File Locations

| What | Location |
|------|----------|
| Main App | `app.py` |
| Sample Data | `data/sample_financials.csv` |
| Core Logic | `utils/financial_calculator.py` |
| LLM Integration | `utils/llm_handler.py` |
| Documentation | `README.md` | `SETUP.md` |

### Helpful Websites

- Python: https://python.org
- Streamlit: https://streamlit.io
- Anthropic: https://anthropic.com
- Plotly: https://plotly.com
- Pandas: https://pandas.pydata.org

---

## Getting Help

1. **Check Errors**: Read the error message carefully
2. **Verify Setup**: Follow steps again from beginning
3. **Check Documentation**: Review README.md and module docstrings
4. **Search Online**: Copy error message into Google
5. **Documentation**: Visit official package documentation

---

**Setup should take 15-30 minutes total**

Once complete, you'll have a full working AI-powered equity research tool! 🎉
