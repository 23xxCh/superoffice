"""
Image Generation API Client - MiniMax and SenseNova
"""

import os
import json
import base64
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Union
from dataclasses import dataclass
import httpx


@dataclass
class ImageGenerationConfig:
    """Configuration for image generation"""
    minimax_api_key: str = ""
    sensenova_api_key: str = ""
    minimax_base_url: str = "https://api.minimax.chat/v1"
    sensenova_base_url: str = "https://token.sensenova.cn/v1"
    default_size: str = "1024x1024"
    default_quality: str = "standard"


class MiniMaxClient:
    """MiniMax API client for image generation"""

    def __init__(self, api_key: str, base_url: str = "https://api.minimax.chat/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=120.0)

    async def generate_image(
        self,
        prompt: str,
        model: str = "image-01",
        size: str = "1024x1024",
        quality: str = "standard",
        num_images: int = 1
    ) -> Dict:
        """Generate image using MiniMax API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "num_images": num_images
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/image/generation",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e), "status_code": e.response.status_code if e.response else None}

    async def recognize_image(
        self,
        image: str,
        prompt: str = "Describe this image in detail"
    ) -> Dict:
        """Analyze image using MiniMax Vision API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "MiniMax-VL",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": prompt}
                    ]
                }
            ]
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}

    async def close(self):
        await self.client.aclose()


class SenseNovaClient:
    """SenseNova API client for image generation"""

    def __init__(self, api_key: str, base_url: str = "https://token.sensenova.cn/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=120.0)

    async def generate_image(
        self,
        prompt: str,
        model: str = "sensenova-u1-fast",
        size: str = "1024x1024",
        **kwargs
    ) -> Dict:
        """Generate image using SenseNova API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            **kwargs
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/image/generation",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}

    async def recognize_image(
        self,
        image: str,
        prompt: str = "Describe this image"
    ) -> Dict:
        """Analyze image using SenseNova Vision API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "sensenova-6.7b-vision",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image}},
                        {"type": "text", "text": prompt}
                    ]
                }
            ]
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}

    async def close(self):
        await self.client.aclose()


class ImageGenerator:
    """Unified image generation client"""

    def __init__(self, config: Optional[ImageGenerationConfig] = None):
        self.config = config or ImageGenerationConfig()
        self._minimax_client: Optional[MiniMaxClient] = None
        self._sensenova_client: Optional[SenseNovaClient] = None

    @property
    def minimax_client(self) -> Optional[MiniMaxClient]:
        if not self._minimax_client and self.config.minimax_api_key:
            self._minimax_client = MiniMaxClient(
                self.config.minimax_api_key,
                self.config.minimax_base_url
            )
        return self._minimax_client

    @property
    def sensenova_client(self) -> Optional[SenseNovaClient]:
        if not self._sensenova_client and self.config.sensenova_api_key:
            self._sensenova_client = SenseNovaClient(
                self.config.sensenova_api_key,
                self.config.sensenova_base_url
            )
        return self._sensenova_client

    async def generate(
        self,
        prompt: str,
        provider: str = "minimax",
        model: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Generate image with specified provider"""
        if provider.lower() == "minimax":
            if not self.minimax_client:
                return {"error": "MiniMax API key not configured"}
            return await self.minimax_client.generate_image(
                prompt,
                model=model or "image-01",
                size=kwargs.get("size", self.config.default_size),
                quality=kwargs.get("quality", self.config.default_quality)
            )
        elif provider.lower() == "sensenova":
            if not self.sensenova_client:
                return {"error": "SenseNova API key not configured"}
            return await self.sensenova_client.generate_image(
                prompt,
                model=model or "sensenova-u1-fast",
                size=kwargs.get("size", self.config.default_size)
            )
        else:
            return {"error": f"Unknown provider: {provider}"}

    async def generate_batch(
        self,
        prompts: List[str],
        provider: str = "minimax",
        **kwargs
    ) -> List[Dict]:
        """Generate multiple images"""
        results = []
        for prompt in prompts:
            result = await self.generate(prompt, provider, **kwargs)
            results.append(result)
        return results

    async def recognize(
        self,
        image: str,
        prompt: str = "Describe this image in detail",
        provider: str = "minimax"
    ) -> Dict:
        """Analyze image"""
        if provider.lower() == "minimax":
            if not self.minimax_client:
                return {"error": "MiniMax API key not configured"}
            return await self.minimax_client.recognize_image(image, prompt)
        elif provider.lower() == "sensenova":
            if not self.sensenova_client:
                return {"error": "SenseNova API key not configured"}
            return await self.sensenova_client.recognize_image(image, prompt)
        else:
            return {"error": f"Unknown provider: {provider}"}

    async def close(self):
        """Close all clients"""
        if self._minimax_client:
            await self._minimax_client.close()
        if self._sensenova_client:
            await self._sensenova_client.close()


# Synchronous wrapper for CLI usage
class SyncImageGenerator:
    """Synchronous wrapper for ImageGenerator"""

    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()

        config = ImageGenerationConfig(
            minimax_api_key=os.getenv("MINIMAX_API_KEY", ""),
            sensenova_api_key=os.getenv("SENSENOVA_API_KEY", ""),
            minimax_base_url=os.getenv("MINIMAX_API_BASE", "https://api.minimax.chat/v1"),
            sensenova_base_url=os.getenv("SENSENOVA_API_BASE", "https://token.sensenova.cn/v1")
        )
        self.async_generator = ImageGenerator(config)

    def generate(self, prompt: str, provider: str = "minimax", **kwargs) -> Dict:
        """Synchronous generate"""
        return asyncio.run(self.async_generator.generate(prompt, provider, **kwargs))

    def generate_batch(self, prompts: List[str], provider: str = "minimax", **kwargs) -> List[Dict]:
        """Synchronous batch generate"""
        return asyncio.run(self.async_generator.generate_batch(prompts, provider, **kwargs))

    def recognize(self, image: str, prompt: str = "Describe this image", provider: str = "minimax") -> Dict:
        """Synchronous recognize"""
        return asyncio.run(self.async_generator.recognize(image, prompt, provider))


# CLI entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python image_gen.py <command> [args...]")
        print("Commands: generate, batch, recognize")
        sys.exit(1)

    command = sys.argv[1]
    generator = SyncImageGenerator()

    if command == "generate":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "a beautiful sunset"
        provider = sys.argv[3] if len(sys.argv) > 3 else "minimax"
        print(json.dumps(generator.generate(prompt, provider), indent=2, default=str))
    elif command == "batch":
        prompts = sys.argv[2].split(",") if len(sys.argv) > 2 else ["a cat", "a dog"]
        print(json.dumps(generator.generate_batch(prompts), indent=2, default=str))
    elif command == "recognize":
        image = sys.argv[2] if len(sys.argv) > 2 else ""
        prompt = sys.argv[3] if len(sys.argv) > 3 else "Describe this image"
        print(json.dumps(generator.recognize(image, prompt), indent=2, default=str))