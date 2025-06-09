"""
Inference client that abstracts different model servers
Supports llama.cpp, ollama, vllm, and future backends
"""

import httpx
import json
from typing import AsyncGenerator, Dict, Any, Optional
from abc import ABC, abstractmethod
import subprocess
import asyncio

from config import settings, ModelServer

class InferenceClient(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def stream_generate(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        pass

class LlamaCppClient(InferenceClient):
    """Client for llama.cpp server running on Raspberry Pi"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=settings.api_timeout)
    
    async def generate(self, prompt: str, **kwargs) -> str:
        payload = {
            "prompt": prompt,
            "n_predict": kwargs.get("max_tokens", settings.max_tokens),
            "temperature": kwargs.get("temperature", settings.temperature),
            "stop": kwargs.get("stop", []),
            "stream": False
        }
        
        response = await self.client.post(
            f"{self.base_url}/completion",
            json=payload
        )
        response.raise_for_status()
        
        result = response.json()
        return result.get("content", "")
    
    async def stream_generate(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        payload = {
            "prompt": prompt,
            "n_predict": kwargs.get("max_tokens", settings.max_tokens),
            "temperature": kwargs.get("temperature", settings.temperature),
            "stop": kwargs.get("stop", []),
            "stream": True
        }
        
        async with self.client.stream(
            "POST",
            f"{self.base_url}/completion",
            json=payload
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if "content" in data:
                        yield data["content"]

class LocalPiClient(InferenceClient):
    """Direct client using tangnet alias on local Pi"""
    
    async def generate(self, prompt: str, **kwargs) -> str:
        # SSH into Pi and run tangnet command
        cmd = f'ssh brand@192.168.1.31 "tangnet \\"{prompt}\\""'
        
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await proc.communicate()
        
        if proc.returncode != 0:
            raise Exception(f"Failed to run tangnet: {stderr.decode()}")
        
        return stdout.decode().strip()
    
    async def stream_generate(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        # For now, just yield the full response
        response = await self.generate(prompt, **kwargs)
        yield response

class OllamaClient(InferenceClient):
    """Client for Ollama (future 3080 setup)"""
    
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient(timeout=settings.api_timeout)
    
    async def generate(self, prompt: str, **kwargs) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", settings.temperature),
                "num_predict": kwargs.get("max_tokens", settings.max_tokens)
            }
        }
        
        response = await self.client.post(
            f"{self.base_url}/api/generate",
            json=payload
        )
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "")
    
    async def stream_generate(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": kwargs.get("temperature", settings.temperature),
                "num_predict": kwargs.get("max_tokens", settings.max_tokens)
            }
        }
        
        async with self.client.stream(
            "POST",
            f"{self.base_url}/api/generate",
            json=payload
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                data = json.loads(line)
                if "response" in data:
                    yield data["response"]

def get_inference_client() -> InferenceClient:
    """Factory function to get the appropriate inference client"""
    
    if settings.active_server == ModelServer.LOCAL_PI:
        # Check if llama.cpp server is running, otherwise use SSH
        try:
            # Try to connect to llama.cpp server
            return LlamaCppClient(settings.local_pi_url)
        except:
            # Fallback to SSH
            return LocalPiClient()
    
    elif settings.active_server == ModelServer.REMOTE_3080:
        # Future 3080 setup - could be llama.cpp or ollama
        return OllamaClient(settings.remote_3080_url, settings.remote_3080_model)
    
    elif settings.active_server == ModelServer.OLLAMA:
        return OllamaClient(settings.ollama_url, settings.remote_3080_model)
    
    elif settings.active_server == ModelServer.VLLM:
        # TODO: Implement vLLM client
        raise NotImplementedError("vLLM client not yet implemented")
    
    else:
        raise ValueError(f"Unknown server type: {settings.active_server}")