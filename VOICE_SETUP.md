# Installing PyAudio for Voice Support

## The Problem
PyAudio requires the correct version for your Python. You have **Python 3.14**.

## Solution: Download Correct PyAudio Wheel

### Step 1: Download
Go to: **https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio**

Find and download:
```
PyAudio‑0.2.14‑cp314‑cp314‑win_amd64.whl
```
(Note: **cp314** means Python 3.14, **win_amd64** means 64-bit Windows)

### Step 2: Install
```bash
pip install C:\Users\syedn\Downloads\PyAudio‑0.2.14‑cp314‑cp314‑win_amd64.whl
```

### Step 3: Restart Anna
```bash
python main.py
```

## Alternative: Try pipwin with full path

Sometimes pipwin needs the full path:

```bash
python -m pipwin install pyaudio
```

## What You'll Get After Installing

✅ "Hey Anna" wake word detection
✅ Voice commands (speak naturally)
✅ Text-to-speech responses
✅ Background listening (always ready)

## Current Status Without PyAudio

Right now Anna works perfectly with:
- ✅ GUI interface
- ✅ Type commands
- ✅ All automation
- ❌ No voice input

Voice will work immediately after PyAudio is installed!
