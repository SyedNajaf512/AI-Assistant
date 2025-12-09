# Quick Fix for PyAudio Installation Issue

## Problem
PyAudio requires Microsoft Visual C++ Build Tools to compile, which caused the installation to fail.

## Solution: Install Pre-built PyAudio

### Option A: Use pipwin (Easiest)
```bash
pip install pipwin
pipwin install pyaudio
```

### Option B: Manual Wheel Download
1. Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Download the wheel for Python 3.14, 64-bit:
   - `PyAudio‑0.2.14‑cp314‑cp314‑win_amd64.whl`
3. Install it:
   ```bash
   pip install path/to/PyAudio‑0.2.14‑cp314‑cp314‑win_amd64.whl
   ```

### Option C: Install without PyAudio (Voice will be disabled)
Edit `requirements.txt` and comment out the pyaudio line:
```
# pyaudio>=0.2.13
```

Then run:
```bash
pip install -r requirements.txt
```

## After Fixing PyAudio

Continue with setup:
```bash
# Create .env file
copy .env.example .env

# Edit .env and add your Gemini API key
# Then run Anna:
python main.py
```

## If Voice Still Doesn't Work

The system will run with all other features (GUI, automation) even without PyAudio. Voice commands just won't be available.
