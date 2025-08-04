# 🚀 Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
python setup.py
```
Or manually:
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
1. Copy the environment template:
```bash
cp env_template.txt .env
```

2. Edit `.env` and add your Murf API key:
```
MURF_API_KEY=your_actual_api_key_here
```

### 3. Start the Server
```bash
python main.py
```

## Testing

### Option 1: FastAPI Docs (Recommended)
1. Open http://localhost:8000/docs in your browser
2. Click on the `/tts` endpoint
3. Click "Try it out"
4. Enter test data:
```json
{
  "text": "Hello! This is a test message.",
  "voice_id": "en-US-Neural2-F"
}
```
5. Click "Execute"

### Option 2: Web Interface
1. Open `test_page.html` in your browser
2. Enter text and click "Generate Speech"

### Option 3: Command Line
```bash
python test_tts.py
```

## Expected Response
```json
{
  "success": true,
  "audio_url": "https://example.com/audio-file.mp3",
  "error": null
}
```

## Troubleshooting

- **"MURF_API_KEY not configured"**: Add your API key to the `.env` file
- **"Server is not running"**: Start the server with `python main.py`
- **Network errors**: Check your internet connection and API key validity

## LinkedIn Screenshots

For your LinkedIn post, capture:
1. FastAPI docs interface at `/docs`
2. Successful TTS response with audio URL
3. Server code (without API keys)
4. Project structure

**Remember**: Never include API keys in screenshots! 