"""
Video Generation API Client - MiniMax Hailuo
"""

import os
import json
import asyncio
import time
from typing import Optional, List, Dict
from dataclasses import dataclass
import httpx


@dataclass
class VideoGenerationConfig:
    """Configuration for video generation"""
    api_key: str = ""
    base_url: str = "https://api.minimax.chat/v1"
    default_model: str = "MiniMax-Hailuo-2.3"
    poll_interval: int = 5  # seconds
    max_wait: int = 300  # seconds


class VideoGenerator:
    """MiniMax Hailuo video generation client"""

    def __init__(self, config: Optional[VideoGenerationConfig] = None):
        self.config = config or VideoGenerationConfig()
        self.client = httpx.AsyncClient(timeout=300.0)

    def _get_headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_video(
        self,
        prompt: str,
        model: str = "MiniMax-Hailuo-2.3",
        duration: int = 5,
        resolution: str = "720p",
        **kwargs
    ) -> Dict:
        """Generate video from text prompt"""
        if not self.config.api_key:
            return {"error": "API key not configured"}

        payload = {
            "model": model,
            "prompt": prompt,
            "duration": duration,
            "resolution": resolution,
            **kwargs
        }

        try:
            response = await self.client.post(
                f"{self.config.base_url}/video/generation",
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            result = response.json()

            # If task is async, return task_id for polling
            if "task_id" in result:
                return {
                    "task_id": result["task_id"],
                    "status": "processing",
                    "message": "Video generation started. Use get_video_status() to check progress."
                }

            return result

        except httpx.HTTPError as e:
            return {"error": str(e), "status_code": e.response.status_code if e.response else None}

    async def generate_from_image(
        self,
        image: str,
        prompt: str,
        model: str = "MiniMax-Hailuo-2.3",
        duration: int = 5,
        **kwargs
    ) -> Dict:
        """Generate video from static image"""
        if not self.config.api_key:
            return {"error": "API key not configured"}

        payload = {
            "model": model,
            "image": image,
            "prompt": prompt,
            "duration": duration,
            **kwargs
        }

        try:
            response = await self.client.post(
                f"{self.config.base_url}/videogeneration/image-to-video",
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            result = response.json()

            if "task_id" in result:
                return {
                    "task_id": result["task_id"],
                    "status": "processing"
                }

            return result

        except httpx.HTTPError as e:
            return {"error": str(e)}

    async def generate_with_subject(
        self,
        subject_image: str,
        prompt: str,
        model: str = "MiniMax-Hailuo-2.3",
        **kwargs
    ) -> Dict:
        """Generate video with subject reference"""
        if not self.config.api_key:
            return {"error": "API key not configured"}

        payload = {
            "model": model,
            "subject_image": subject_image,
            "prompt": prompt,
            **kwargs
        }

        try:
            response = await self.client.post(
                f"{self.config.base_url}/video/generation/with-subject",
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            return {"error": str(e)}

    async def get_task_status(self, task_id: str) -> Dict:
        """Get status of async video generation task"""
        try:
            response = await self.client.get(
                f"{self.config.base_url}/video/tasks/{task_id}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            return {"error": str(e)}

    async def wait_for_video(self, task_id: str) -> Dict:
        """Wait for video generation to complete"""
        start_time = time.time()

        while time.time() - start_time < self.config.max_wait:
            status = await self.get_task_status(task_id)

            if status.get("status") == "completed":
                return {
                    "status": "completed",
                    "video_url": status.get("video_url"),
                    "video_path": status.get("video_path")
                }
            elif status.get("status") == "failed":
                return {
                    "status": "failed",
                    "error": status.get("error", "Unknown error")
                }

            await asyncio.sleep(self.config.poll_interval)

        return {"status": "timeout", "error": "Max wait time exceeded"}

    async def use_template(
        self,
        template_id: str,
        prompt: str,
        **kwargs
    ) -> Dict:
        """Generate video using template"""
        if not self.config.api_key:
            return {"error": "API key not configured"}

        payload = {
            "template_id": template_id,
            "prompt": prompt,
            **kwargs
        }

        try:
            response = await self.client.post(
                f"{self.config.base_url}/video/generation/template",
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            return {"error": str(e)}

    async def process_video(
        self,
        video_path: str,
        operation: str,
        **kwargs
    ) -> Dict:
        """Process video with ffmpeg"""
        import subprocess
        from pathlib import Path

        input_path = Path(video_path)
        if not input_path.exists():
            return {"error": f"Video not found: {video_path}"}

        output_path = input_path.parent / f"{input_path.stem}_{operation}{input_path.suffix}"

        try:
            if operation == "trim":
                start = kwargs.get("start", 0)
                end = kwargs.get("end", 10)
                cmd = ["ffmpeg", "-i", str(input_path), "-ss", str(start), "-to", str(end), "-c", "copy", str(output_path)]
            elif operation == "concat":
                # For concat, need multiple videos
                videos = kwargs.get("videos", [])
                # Create concat file
                concat_file = input_path.parent / "concat.txt"
                with open(concat_file, "w") as f:
                    for v in videos:
                        f.write(f"file '{v}'\n")
                cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(output_path)]
            elif operation == "extract":
                timestamp = kwargs.get("timestamp", 0)
                cmd = ["ffmpeg", "-i", str(input_path), "-ss", str(timestamp), "-vframes", "1", str(output_path)]
            elif operation == "convert":
                target_format = kwargs.get("format", "mp4")
                output_path = input_path.with_suffix(f".{target_format}")
                cmd = ["ffmpeg", "-i", str(input_path), str(output_path)]
            else:
                return {"error": f"Unknown operation: {operation}"}

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                return {"status": "success", "output": str(output_path)}
            else:
                return {"error": result.stderr}

        except Exception as e:
            return {"error": str(e)}

    async def close(self):
        await self.client.aclose()


# Synchronous wrapper
class SyncVideoGenerator:
    """Synchronous wrapper for VideoGenerator"""

    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()

        config = VideoGenerationConfig(
            api_key=os.getenv("MINIMAX_API_KEY", ""),
            base_url=os.getenv("MINIMAX_API_BASE", "https://api.minimax.chat/v1")
        )
        self.async_generator = VideoGenerator(config)

    def generate(self, prompt: str, **kwargs) -> Dict:
        return asyncio.run(self.async_generator.generate_video(prompt, **kwargs))

    def generate_from_image(self, image: str, prompt: str, **kwargs) -> Dict:
        return asyncio.run(self.async_generator.generate_from_image(image, prompt, **kwargs))

    def wait_for(self, task_id: str) -> Dict:
        return asyncio.run(self.async_generator.wait_for_video(task_id))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python video_gen.py <command> [args...]")
        sys.exit(1)

    command = sys.argv[1]
    generator = SyncVideoGenerator()

    if command == "generate":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "a cat playing"
        print(json.dumps(generator.generate(prompt), indent=2, default=str))
    elif command == "image":
        image = sys.argv[2] if len(sys.argv) > 2 else ""
        prompt = sys.argv[3] if len(sys.argv) > 3 else "movement description"
        print(json.dumps(generator.generate_from_image(image, prompt), indent=2, default=str))