---
name: image-generation
description: AI image generation using MiniMax and SenseNova APIs
triggers:
  - /image
  - /draw
  - generate image
  - create image
  - text to image
metadata:
  tier: 1
  category: ai-media
  visibility: public
---

# Image Generation Skill

AI-powered image generation using MiniMax and SenseNova APIs.

## Supported Providers

### MiniMax (Primary)
- **Model**: image-01
- **API**: https://api.minimax.chat/v1
- **Features**: High-quality text-to-image

### SenseNova (Backup)
- **Model**: sensenova-u1-fast
- **API**: https://token.sensenova.cn/v1
- **Features**: Fast generation

## Tools

### generate_image(prompt, provider='minimax', model=None, **kwargs)
Generate image from text prompt.
- prompt: Text description of desired image
- provider: 'minimax' or 'sensenova'
- model: specific model to use
- size: image dimensions (optional)
- quality: 'standard' or 'high' (optional)
- returns: image URL or base64

### generate_image_batch(prompts, provider='minimax')
Generate multiple images from prompts.
- prompts: list of prompt strings
- returns: list of image URLs

### recognize_image(image_url or image_path, prompt=None)
Analyze image using VLM.
- image_url: URL or local path
- prompt: specific question about the image
- returns: description or analysis

### style_imitate(reference_image, prompt)
Generate image in style of reference.
- reference_image: path or URL to reference
- prompt: content description
- returns: styled image

### optimize_prompt(prompt)
Optimize image prompt using LLM.
- prompt: raw prompt
- returns: enhanced prompt

## Usage Examples

### Generate image
```
/image generate a futuristic city at sunset with neon lights
```

### Generate with size
```
/image generate a cat sitting on a chair size 1024x1024
```

### Batch generate
```
/image batch generate ["dog", "cat", "bird"]
```

### Recognize image
```
/image recognize https://example.com/image.jpg describe the scene
```

### Style imitation
```
/image imitate https://example.com/style.jpg a modern car
```

## API Configuration

Set in `.env`:
```
MINIMAX_API_KEY=sk-cp-2_EEt5pGYO_3Hi-RnszXjWaLysv7XBdfBKkKM0_LseLcy273su4m7mwir1Eci_V3WxlDQeCKAvzK9DU0wdQN1zcsJLyTpwIY7FibhbZALCP5MAn04WumveY
SENSENOVA_API_KEY=sk-rOIzAlaxzLhpxS2nqHqXNEuNQSnQDs4q
```

## Models

| Provider | Model | Description |
|----------|-------|-------------|
| MiniMax | image-01 | Latest high-quality model |
| MiniMax | image-01-preview | Preview version |
| SenseNova | sensenova-u1-fast | Fast generation |
| SenseNova | sensenova-u1 | Standard quality |

## Requirements

- Python 3.10+
- httpx
- PIL/Pillow
- python-dotenv