# <img src="icon.png" alt="SafeSoul AI logo" width="32" style="vertical-align:middle; margin-right:8px;"> SafeSoul AI – Mental Health Support Chatbot
## Complete Setup & Requirements Guide

> ✨ *"Your AI-powered companion for compassionate, anonymous mental wellness support."*

---

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Installation Steps](#installation-steps)
4. [Environment Configuration](#environment-configuration)
5. [Running the Project](#running-the-project)
6. [Project Structure](#project-structure)
7. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Minimum System Specifications
- **OS**: Windows 10/11, macOS, or Linux
- **RAM**: 4 GB (8 GB recommended)
- **Disk Space**: 2 GB free
- **Python**: 3.11+ (3.11 recommended)
- **Internet**: Required for Google Gemini API calls

### Supported Platforms
- ✅ Windows (10, 11)
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu, Debian, etc.)

---

## 📦 Prerequisites

You must install the following before running the project:

### 1. **Python 3.11+**
   - Download from: https://www.python.org/downloads/
   - **Verify Installation:**
     ```bash
     python --version
     ```
   - Should output: `Python 3.11.x` or higher

### 2. **pip** (Python Package Manager)
   - Usually comes with Python
   - **Verify Installation:**
     ```bash
     pip --version
     ```

### 3. **Git** (Optional but recommended)
   - Download from: https://git-scm.com/download/

### 4. **Google Gemini API Key**
   - Go to: https://ai.google.dev/
   - Click "Get API Key"
   - Create a new API key
   - **Keep this key safe** – you'll need it for configuration

---

## 🚀 Installation Steps

### Step 1: Clone or Download the Project
```bash
# Using Git (if installed)
git clone <repository-url>
cd Capstone-Project--MHS_Chatbot-main

# Or manually download and extract the ZIP file
```

### Step 2: Create a Virtual Environment
A virtual environment isolates project dependencies from your system Python.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal after activation.

### Step 3: Upgrade pip
```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs all required packages listed below.

---

## 📝 Dependencies

### Core Dependencies (from requirements.txt)

| Package | Version | Purpose |
|---------|---------|---------|
| **streamlit** | 1.31.1 | Web UI framework |
| **python-dotenv** | 1.0.0 | Environment variable management |
| **google-generativeai** | 0.3.2 | Google Gemini API client |
| **pandas** | 2.2.1 | Data manipulation & analysis |
| **numpy** | 1.26.4 | Numerical computations |
| **scikit-learn** | 1.4.1.post1 | Machine learning utilities |
| **nltk** | 3.8.1 | Natural Language Processing |
| **sentence-transformers** | 2.6.1 | Embeddings & sentiment analysis |
| **joblib** | 1.4.0 | Serialization & caching |
| **pickle-mixin** | 1.0.2 | Pickle utilities |

### Optional Dependencies
- **streamlit-extras**: For advanced Streamlit components
- **scipy**: For advanced NLP operations

---

## ⚙️ Environment Configuration

### Step 1: Create `.env` File
In the project root directory, create a file named `.env`:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_api_key_here
```

### Step 2: Add Your Gemini API Key
1. Go to https://ai.google.dev/
2. Get your API key
3. Replace `your_api_key_here` with your actual key
4. **DO NOT commit .env to version control**

### Example .env File
```env
# API Keys
GEMINI_API_KEY=AIzaSyD_example_key_12345

# Optional Configurations
DEBUG=False
SESSION_TIMEOUT=1800
```

---

## ▶️ Running the Project

### Method 1: Using Streamlit (Recommended)
```bash
# Make sure virtual environment is activated
streamlit run main.py
```

The application will open in your browser at:
```
http://localhost:8501
```

### Method 2: Using Batch File (Windows Only)
```bash
# Simply double-click or run:
run_project.bat
```

### Method 3: Manual Python Execution
```bash
python main.py
```

---

## 📁 Project Structure

```
Capstone-Project--MHS_Chatbot-main/
│
├── main.py                    # Main Streamlit application
├── main_f.py                  # Alternative main file
├── gemini.py                  # Google Gemini API integration
├── database.py                # Database operations
├── import os.py               # Utility imports
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore file
├── README.md                  # Original README
├── README_SETUP.md            # This file
└── icon.png                   # UI Banner image
```

### File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Main Streamlit web application |
| `gemini.py` | Handles Google Gemini API calls & response generation |
| `database.py` | Manages database operations & data persistence |
| `requirements.txt` | Lists all Python package dependencies |
| `.env` | Stores sensitive configuration (API keys) |

---

## ✨ Features

### Core Features
- 💬 **Empathetic Conversations**: AI-powered responses using Google Gemini
- 🧠 **Sentiment Detection**: Analyzes emotional state using embeddings
- 🆘 **Crisis Detection**: Identifies crisis situations and suggests help
- 🔒 **Privacy-First**: Anonymous, no login required
- 🧘 **Coping Strategies**: CBT/DBT-based therapeutic suggestions
- 📲 **Quick Prompts**: Pre-built conversation starters
- 📊 **Feedback System**: Rate responses for improvement
- 🌐 **Responsive UI**: Works on desktop and mobile browsers

### Technology Stack
- **Frontend**: Streamlit (Python-based web UI)
- **AI/ML**: 
  - Google Gemini API (response generation)
  - Sentence Transformers (sentiment analysis)
  - scikit-learn (classification)
  - NLTK (NLP processing)
- **Backend**: Python 3.11+
- **Data Handling**: pandas, numpy, joblib

---

## 🔧 Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:**
```bash
pip install -r requirements.txt
```
Ensure virtual environment is activated.

### Problem: API Key Error
**Solution:**
1. Verify `.env` file exists in project root
2. Check API key is correct and enabled
3. Ensure `python-dotenv` is installed: `pip install python-dotenv`
4. Restart Streamlit application: `streamlit run main.py`

### Problem: `GEMINI_API_KEY` not found
**Solution:**
1. Create `.env` file (if missing)
2. Add: `GEMINI_API_KEY=your_key_here`
3. Run: `streamlit run main.py`

### Problem: Port 8501 Already in Use
**Solution:**
```bash
streamlit run main.py --logger.level=debug --server.port 8502
```

### Problem: Slow Response Generation
**Solution:**
- Check internet connection
- Verify Google Gemini API is working
- Check API rate limits
- Run on machine with better specs

### Problem: Virtual Environment Won't Activate
**Windows:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
venv\Scripts\activate
```

**macOS/Linux:**
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

### Problem: Import Errors
**Solution:**
```bash
# Reinstall all dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## 🧪 Verification Checklist

Before running the application, verify:

- ✅ Python 3.11+ installed: `python --version`
- ✅ Virtual environment created and activated: `(venv)` visible in terminal
- ✅ Dependencies installed: `pip list | grep streamlit`
- ✅ `.env` file created with API key
- ✅ API key is valid and active
- ✅ Internet connection available

---

## 🌐 Deployment Options

### Local Deployment
- ✅ Already covered (just run `streamlit run main.py`)

### Cloud Deployment
- **Streamlit Cloud**: https://streamlit.io/cloud
- **Heroku**: With Procfile configuration
- **AWS/Azure**: With containerization
- **Google Cloud**: App Engine or Cloud Run

---

## 📞 Support & Troubleshooting

### Common Questions

**Q: Do I need to sign up for Gemini API?**
A: Yes, you need a Google account and an API key from https://ai.google.dev/

**Q: Is my data stored?**
A: No, SafeSoul AI is privacy-first. No personal data is stored.

**Q: Can I run this offline?**
A: No, this version requires internet for Google Gemini API.

**Q: What Python version do I need?**
A: Python 3.11 or higher recommended. 3.10+ may work but not tested.

---

## 📋 Additional Notes

### Performance Tips
- Use Python 3.11+ for better performance
- 8GB+ RAM recommended for smooth operation
- Stable internet connection required

### Security Best Practices
- Never commit `.env` file to Git
- Don't share your API key publicly
- Regenerate API key if compromised
- Use `.gitignore` to exclude sensitive files

### First-Time Users
1. Read this entire document
2. Follow installation steps exactly
3. Run verification checklist
4. Start with `streamlit run main.py`
5. Check terminal for error messages

---

## 🔐 Privacy & Ethics

- ✅ No login or registration required
- 🔐 No personal data collection
- 30-minute session expiration (auto-wipe)
- ⚖️ GDPR & HIPAA compliant policies
- 🛑 Not a replacement for professional therapy


---


## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---
