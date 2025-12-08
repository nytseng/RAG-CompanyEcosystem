import os
import requests
import asyncio
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from openai import OpenAI, AsyncOpenAI
import anthropic
from anthropic import AsyncAnthropic
from google import genai

from base_evaluator import BaseEvaluator


# =========================
# LLM Clients
# =========================
class LLMClient(ABC):
    """Base interface for any LLM client."""

    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> str:
        """Generate a text response from a list of messages."""
        ...

    async def agenerate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> str:
        """
        Default async version that just runs the sync generate() in a worker
        thread. Subclasses with native async SDKs can override this.
        """
        return await asyncio.to_thread(self.generate, messages, temperature, max_tokens)



class OpenAIClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.provider = "openai"

    def generate(self, messages, temperature=0.7, max_tokens=512) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    async def agenerate(self,messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 512) -> str:
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content


class ClaudeClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.async_client = AsyncAnthropic(api_key=api_key)
        self.model = model
        self.provider = "anthropic"

    def generate(self, messages, temperature=0.7, max_tokens=512) -> str:
        # Anthropic API uses a different schema; map simple chat format.
        formatted_msgs = []
        for m in messages:
            if m["role"] == "system":
                formatted_msgs.append(
                    {"role": "user", "content": f"System note: {m['content']}"}
                )
            else:
                formatted_msgs.append(m)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=formatted_msgs,
        )
        return response.content[0].text

    async def agenerate(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 512) -> str:
        formatted_msgs = []
        for m in messages:
            if m["role"] == "system":
                formatted_msgs.append(
                    {"role": "user", "content": f"System note: {m['content']}"}
                )
            else:
                formatted_msgs.append(m)

        response = await self.async_client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=formatted_msgs,
        )
        return response.content[0].text

class GeminiClient(LLMClient):
    """
    LLMClient implementation for Google's Gemini models using the
    official google-genai SDK.

    Expects the API key in GEMINI_API_KEY by default.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash",):
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.async_client = self.client.aio
        self.model = model
        self.provider = "google"

    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 512) -> str:
        prompt_lines = [
            f"{m['role'].upper()}: {m['content']}" for m in messages if "content" in m
        ]
        prompt_text = "\n".join(prompt_lines)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt_text,
            config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )
        return response.text

    async def agenerate(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 512) -> str:
        prompt_lines = [
            f"{m['role'].upper()}: {m['content']}" for m in messages if "content" in m
        ]
        prompt_text = "\n".join(prompt_lines)

        response = await self.async_client.models.generate_content(
            model=self.model,
            contents=prompt_text,
            config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )
        return response.text

class LocalLLMClient(LLMClient):
    def __init__(self, host: str = "http://localhost:8000/v1/chat/completions", model: str = "llama-3-70b"):
        self.host = host
        self.model = model

    def generate(self, messages, temperature=0.7, max_tokens=512) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_new_tokens": max_tokens,
        }
        response = requests.post(self.host, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    async def agenerate(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 512) -> str:
        return await asyncio.to_thread(self.generate, messages, temperature, max_tokens)


class LLMEvaluator(BaseEvaluator):
    """
    Evaluates factuality between RAG-generated answers and a synthetic reference
    (constructed from the golden documents).
    """

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def _make_reference(self, gold_documents: List[Dict]) -> str:
        return " ".join(self.parse_document_text(doc) for doc in gold_documents).strip()

    def evaluate(
        self,
        question: str,
        response: str,
        gold_documents: List[Dict],
        retrieved_context: List[Dict],
        reference_answer: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Compare the factuality between the generated and reference answers.
        Returns a dict with:
          - "llm_factuality_judgement": full LLM response
        """
        reference = reference_answer or self._make_reference(gold_documents)

        prompt = f"""
        You are an expert fact-checker. Compare the following two answers to the same question:

        Question: {question}
        Reference answer (from gold documents): {reference}
        Generated answer: {response}

        Evaluate whether the generated answer is factually correct compared to the reference.
        Only consider factual accuracy, not style or completeness.

        Rate factual accuracy as one of the following:
        - "Correct" (All facts match the reference)
        - "Partially Correct" (Some but not all facts match)
        - "Incorrect" (Facts contradict or miss key points)

        Then explain your reasoning in 2-3 sentences.
        """

        messages = [
            {"role": "system", "content": "You are a careful factuality evaluator for a RAG system."},
            {"role": "user", "content": prompt.strip()},
        ]

        judgement = self.llm.generate(messages)
        return {"llm_factuality_judgement": judgement}
