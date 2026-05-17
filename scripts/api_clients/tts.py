"""
TTS Audio - Text-to-speech synthesis using MiniMax, Edge TTS
"""

import os
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass
import httpx


@dataclass
class TTSConfig:
    """Configuration for TTS"""
    minimax_api_key: str = ""
    edge_voices: str = "zh-CN-Xiaoxiao"
    default_speed: float = 1.0
    default_pitch: float = 0.0


class MiniMaxTTS:
    """MiniMax TTS client"""

    def __init__(self, api_key: str, base_url: str = "https://api.minimax.chat/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)

    def _get_headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def synthesize(
        self,
        text: str,
        voice: str = "female-shaonv",
        speed: float = 1.0,
        pitch: float = 0.0,
        model: str = "speech-2.8-hd"
    ) -> Dict:
        """Synthesize text to speech"""
        if not self.api_key:
            return {"error": "API key not configured"}

        payload = {
            "model": model,
            "text": text,
            "voice_id": voice,
            "speed": speed,
            "pitch": pitch
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/audio/synthesis",
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            result = response.json()

            if "audio_url" in result:
                return {"status": "success", "audio_url": result["audio_url"]}
            elif "task_id" in result:
                return {"task_id": result["task_id"], "status": "processing"}

            return result

        except httpx.HTTPError as e:
            return {"error": str(e)}

    async def list_voices(self) -> Dict:
        """List available MiniMax voices"""
        # This would typically call the API to get voice list
        return {
            "voices": [
                {"id": "male-qn-qingse", "name": "Male Clear", "gender": "male"},
                {"id": "female-shaonv", "name": "Female Youthful", "gender": "female"},
                {"id": "male-qn-jingying", "name": "Male Professional", "gender": "male"},
                {"id": "female-yujie", "name": "Female Elegant", "gender": "female"},
            ]
        }

    async def close(self):
        await self.client.aclose()


class EdgeTTS:
    """Microsoft Edge TTS client (free)"""

    VOICES = {
        "en-US": ["en-US-Jenny", "en-US-Guy", "en-US-Aria"],
        "zh-CN": ["zh-CN-Xiaoxiao", "zh-CN-Yunxi", "zh-CN-Yunyang"],
        "ja-JP": ["ja-JP-Nanami", "ja-JP-Keita"],
        "ko-KR": ["ko-KR-SunHi", "ko-KR-InJoon"],
    }

    @staticmethod
    async def synthesize(
        text: str,
        voice: str = "zh-CN-Xiaoxiao",
        output_path: str = "output.mp3",
        speed: str = "+0%",
        pitch: str = "+0Hz"
    ) -> Dict:
        """Synthesize using Edge TTS"""
        try:
            import edge_tts

            # Create communicator
            communicate = edge_tts.Communicate(text, voice, rate=speed, pitch=pitch)

            # Save to file
            await communicate.save(output_path)

            return {"status": "success", "output": output_path}

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    async def list_voices() -> Dict:
        """List all available Edge TTS voices"""
        try:
            voices = await edge_tts.list_voices()
            return {"voices": voices}
        except Exception as e:
            return {"error": str(e)}


class TTSClient:
    """Unified TTS client with multiple providers"""

    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self._minimax_client: Optional[MiniMaxTTS] = None

    @property
    def minimax_client(self) -> Optional[MiniMaxTTS]:
        if not self._minimax_client and self.config.minimax_api_key:
            self._minimax_client = MiniMaxTTS(self.config.minimax_api_key)
        return self._minimax_client

    async def synthesize(
        self,
        text: str,
        provider: str = "minimax",
        voice: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Synthesize text to speech"""
        if provider.lower() == "minimax":
            if not self.minimax_client:
                return {"error": "MiniMax API key not configured"}
            return await self.minimax_client.synthesize(
                text,
                voice=voice or "female-shaonv",
                speed=kwargs.get("speed", 1.0),
                pitch=kwargs.get("pitch", 0.0)
            )
        elif provider.lower() == "edge":
            output_path = kwargs.get("output", "output.mp3")
            return await EdgeTTS.synthesize(
                text,
                voice=voice or self.config.edge_voices,
                output_path=output_path,
                speed=kwargs.get("speed", "+0%"),
                pitch=kwargs.get("pitch", "+0Hz")
            )
        else:
            return {"error": f"Unknown provider: {provider}"}

    async def list_voices(self, provider: str = "minimax") -> Dict:
        """List available voices"""
        if provider.lower() == "minimax":
            if not self.minimax_client:
                return {"error": "MiniMax API key not configured"}
            return await self.minimax_client.list_voices()
        elif provider.lower() == "edge":
            return {"voices": EdgeTTS.VOICES}
        else:
            return {"error": f"Unknown provider: {provider}"}

    async def synthesize_with_timestamps(
        self,
        text: str,
        provider: str = "minimax",
        voice: Optional[str] = None
    ) -> Dict:
        """Generate speech with word-level timestamps"""
        # This is a simplified version - full implementation would use
        # provider-specific APIs for timestamp generation
        result = await self.synthesize(text, provider, voice)

        # Generate dummy timestamps (in real implementation, parse from API)
        words = text.split()
        timestamps = []
        current_time = 0

        for word in words:
            word_duration = len(word) * 0.05  # Approximate
            timestamps.append({
                "word": word,
                "start": current_time,
                "end": current_time + word_duration
            })
            current_time += word_duration + 0.1  # Gap between words

        result["timestamps"] = timestamps
        return result


# Synchronous wrapper
class SyncTTSClient:
    """Synchronous TTS client"""

    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()

        config = TTSConfig(
            minimax_api_key=os.getenv("MINIMAX_API_KEY", "")
        )
        self.async_client = TTSClient(config)

    def synthesize(self, text: str, provider: str = "minimax", **kwargs) -> Dict:
        return asyncio.run(self.async_client.synthesize(text, provider, **kwargs))

    def list_voices(self, provider: str = "minimax") -> Dict:
        return asyncio.run(self.async_client.list_voices(provider))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tts.py <command> [args...]")
        print("Commands: synthesize, voices")
        sys.exit(1)

    command = sys.argv[1]
    client = SyncTTSClient()

    if command == "synthesize":
        text = sys.argv[2] if len(sys.argv) > 2 else "Hello world"
        provider = sys.argv[3] if len(sys.argv) > 3 else "edge"
        print(json.dumps(client.synthesize(text, provider), indent=2, default=str))
    elif command == "voices":
        provider = sys.argv[2] if len(sys.argv) > 2 else "edge"
        print(json.dumps(client.list_voices(provider), indent=2, default=str))