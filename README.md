# Real-Time Emoji Expression Detector 😛😲😐

A fun Python app that uses your webcam to detect facial expressions like mouth opening or eyebrow raising in real-time and plays corresponding sounds ("bleeh" or "huhhh") while showing an emoji in a floating GUI window.

---

## 🎯 Features

- Detects:
  - **Mouth Open** ➜ Plays `bleeh.wav` & shows 😛
  - **Eyebrow Raise** ➜ Plays `huhhh.wav` & shows 😲
  - **Neutral Face** ➜ Shows 😐
- Plays sound using `simpleaudio` and `pydub`
- Displays emoji with a floating `tkinter` window
- Uses `mediapipe` for precise face landmark detection

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/emoji-expression-detector.git
cd emoji-expression-detector
```
2. Set up a virtual environment (recommended)
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies
```bash
opencv-python
mediapipe
simpleaudio
pydub
```

If pydub raises an error, you might need to install ffmpeg:

On Windows: Download from https://www.ffmpeg.org/download.html and add it to your system PATH.
```bash
brew install ffmpeg
```
If the sound doesn't play, ensure your default output device is not muted and that simpleaudio supports your OS.
