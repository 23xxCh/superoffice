---
name: music-generation
description: AI music/song generation using MiniMax Music API
triggers:
  - /music
  - generate music
  - create song
  - compose music
metadata:
  tier: 1
  category: ai-media
  visibility: public
---

# Music Generation Skill

AI-powered music and song generation using MiniMax Music API.

## Supported Models

### MiniMax Music
- **music-2.6-free** - Free tier, basic features
- **music-2.6** - Full features
- **music-cover-free** - Cover song generation

## Features

- Text-to-music generation
- Song generation with lyrics
- Instrumental generation
- Cover song generation
- Voice cloning support
- Streaming generation

## Tools

### generate_music(prompt, style=None, duration=60, **kwargs)
Generate music from text prompt.
- prompt: description of desired music
- style: 'pop', 'rock', 'jazz', 'classical', 'electronic', etc.
- duration: length in seconds
- returns: music URL or task_id

### generate_song(lyrics=None, prompt=None, style='pop', **kwargs)
Generate song with lyrics.
- lyrics: song lyrics (optional, can be auto-generated)
- prompt: music description
- style: genre/style
- returns: song URL

### generate_cover(song_url, prompt, **kwargs)
Generate cover version of existing song.
- song_url: URL to source audio
- prompt: description of new style
- returns: cover URL

### generate_instrumental(prompt, style, duration=60)
Generate instrumental music only.
- prompt: music description
- style: genre
- duration: length

### optimize_lyrics(topic, style='pop', mood='upbeat')
Auto-generate song lyrics.
- topic: song theme
- style: genre
- mood: 'upbeat', 'sad', 'romantic', 'energetic'
- returns: generated lyrics

## Usage Examples

### Generate music from prompt
```
/music generate an upbeat electronic dance track duration 30
```

### Generate song with lyrics
```
/music song lyrics="Hello world" style pop
```

### Auto-generate song
```
/music create song about "love and loss" style ballad
```

### Generate instrumental
```
/music instrumental piano jazz 60
```

### Generate cover
```
/music cover https://example.com/song.mp3 "make it more electronic"
```

## Lyrics Generation

The skill can auto-generate lyrics based on:
- Topic/theme
- Style (pop, rock, ballad, etc.)
- Mood (upbeat, sad, romantic, energetic)
- Language support

## API Configuration

Set in `.env`:
```
MINIMAX_API_KEY=sk-cp-2_EEt5pGYO_3Hi-RnszXjWaLysv7XBdfBKkKM0_LseLcy273su4m7mwir1Eci_V3WxlDQeCKAvzK9DU0wdQN1zcsJLyTpwIY7FibhbZALCP5MAn04WumveY
```

## Models

| Model | Description | Features |
|-------|-------------|----------|
| music-2.6-free | Free tier | Basic generation |
| music-2.6 | Full tier | All features |
| music-cover-free | Cover songs | Style transfer |

## Requirements

- Python 3.10+
- httpx
- python-dotenv
- ffmpeg (for audio processing)