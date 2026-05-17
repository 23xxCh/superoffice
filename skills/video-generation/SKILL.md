---
name: video-generation
description: AI video generation using MiniMax Hailuo API
triggers:
  - /video
  - generate video
  - create video
  - text to video
  - image to video
metadata:
  tier: 1
  category: ai-media
  visibility: public
---

# Video Generation Skill

AI-powered video generation using MiniMax Hailuo API.

## Supported Models

### MiniMax Hailuo
- **Hailuo 2.3** - Latest version, high quality
- **Hailuo 2.3-Fast** - Faster generation
- **Hailuo 2.0** - Standard version

## Features

- Text-to-video generation
- Image-to-video generation
- Subject reference (character consistency)
- Template-based generation
- Video processing (concat, trim, extract)

## Tools

### generate_video(prompt, model='hailuo-2.3', **kwargs)
Generate video from text prompt.
- prompt: Text description of desired video
- model: 'hailuo-2.3', 'hailuo-2.3-fast', 'hailuo-2.0'
- duration: video length in seconds (optional)
- resolution: '720p', '1080p' (optional)
- returns: video URL or task_id for async

### generate_video_from_image(image, prompt, model='hailuo-2.3')
Generate video from static image.
- image: URL or local path
- prompt: movement description
- returns: video URL

### generate_with_subject(subject_image, prompt, model='hailuo-2.3')
Generate video with subject reference.
- subject_image: reference character image
- prompt: action/scene description
- returns: video with consistent subject

### use_template(template_id, prompt, **kwargs)
Generate using video template.
- template_id: predefined template ID
- prompt: customized prompt
- returns: templated video

### process_video(video_path, operation, **kwargs)
Process existing video.
- operation: 'concat', 'trim', 'extract', 'convert'
- returns: processed video path

## Usage Examples

### Generate video from text
```
/video generate a cat playing in a garden duration 5
```

### Generate from image
```
/video from image https://example.com/photo.jpg "the person walking"
```

### With subject reference
```
/video with subject reference.jpg "character running in forest"
```

### Use template
```
/video template 001 "beach sunset with waves"
```

### Process video
```
/video process video.mp4 trim start=0 end=10
```

## API Configuration

Set in `.env`:
```
MINIMAX_API_KEY=sk-cp-2_EEt5pGYO_3Hi-RnszXjWaLysv7XBdfBKkKM0_LseLcy273su4m7mwir1Eci_V3WxlDQeCKAvzK9DU0wdQN1zcsJLyTpwIY7FibhbZALCP5MAn04WumveY
```

## Models

| Model | Description | Speed |
|-------|-------------|-------|
| MiniMax-Hailuo-2.3 | Latest, highest quality | Medium |
| MiniMax-Hailuo-2.3-Fast | Fast generation | Fast |
| MiniMax-Hailuo-2.0 | Standard version | Medium |

## Requirements

- Python 3.10+
- httpx
- ffmpeg (for video processing)
- python-dotenv

## Notes

- Video generation is async - returns task_id for polling
- Maximum duration varies by model
- Subject reference requires character image