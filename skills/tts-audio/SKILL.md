---
name: tts-audio
description: Text-to-speech synthesis using MiniMax, Edge TTS, and other providers
triggers:
  - /tts
  - /speak
  - /voice
  - text to speech
  - voice synthesis
metadata:
  tier: 1
  category: ai-media
  visibility: public
---

# TTS Audio Skill

Text-to-speech synthesis using multiple providers.

## Supported Providers

### MiniMax TTS
- **speech-2.8-hd** - High quality, low latency
- **speech-2.6** - Standard quality
- **speech-02** - Latest model
- Voice cloning support

### Edge TTS (Free)
- Microsoft Edge text-to-speech
- 100+ voices, 70+ languages
- No API key required

### ElevenLabs (Optional)
- High quality voice synthesis
- Voice cloning
- Requires API key

## Tools

### synthesize(text, voice=None, provider='minimax', **kwargs)
Convert text to speech.
- text: text to synthesize
- voice: voice ID (provider-specific)
- provider: 'minimax', 'edge', 'elevenlabs'
- speed: speaking rate (optional)
- pitch: voice pitch (optional)
- returns: audio URL or file path

### list_voices(provider='minimax')
List available voices.
- provider: which provider's voices to list
- returns: list of voice options

### clone_voice(audio_samples, name)
Create custom voice from samples.
- audio_samples: list of audio file paths
- name: name for the cloned voice
- returns: voice_id

### synthesize_with_timestamps(text, voice=None)
Generate speech with word-level timestamps.
- For video dubbing, subtitles
- returns: audio + timestamp data

## Usage Examples

### Basic TTS
```
/tts synthesize "Hello world" voice professional
```

### With provider
```
/tts generate "Hello" provider edge voice en-US-Jenny
```

### Clone voice
```
/tts clone voice samples/voice.wav name my_voice
```

### With timestamps
```
/tts timestamps "Hello world" provider minimax
```

## Voice Options

### MiniMax Voices
| Voice ID | Description |
|----------|-------------|
| male-qn-qingse | Male, clear |
| female-shaonv | Female, youthful |
| male-qn-jingying | Male, professional |
| female-yujie | Female, elegant |

### Edge TTS Voices
| Voice | Language |
|-------|----------|
| en-US-Jenny | English (US) |
| zh-CN-Xiaoxiao | Chinese |
| ja-JP-Nanami | Japanese |
| ko-KR-SunHi | Korean |

## API Configuration

Set in `.env`:
```
MINIMAX_API_KEY=sk-cp-2_EEt5pGYO_3Hi-RnszXjWaLysv7XBdfBKkKM0_LseLcy273su4m7mwir1Eci_V3WxlDQeCKAvzK9DU0wdQN1zcsJLyTpwIY7FibhbZALCP5MAn04WumveY
ELEVENLABS_API_KEY=your_key (optional)
```

## Requirements

- Python 3.10+
- httpx
- edge-tts (for Edge TTS)
- python-dotenv
- pydub (for audio processing)