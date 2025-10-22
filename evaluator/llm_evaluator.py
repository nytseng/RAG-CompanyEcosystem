import os
import requests
from openai import OpenAI
from abc import ABC, abstractmethod
from typing import List, Dict
from typing import Optional


# =========================
# Clients class - helper function 
# =========================
class LLMClient(ABC):
    """Base interface for any LLM client."""

    @abstractmethod
    def generate(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 512) -> str:
        """Generate a text response from a list of messages."""
        pass

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def generate(self, messages, temperature=0.7, max_tokens=512):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
class ClaudeClient(LLMClient):
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, messages, temperature=0.7, max_tokens=512):
        formatted_msgs = []
        for m in messages:
            if m["role"] == "system":
                formatted_msgs.append({"role": "user", "content": f"System note: {m['content']}"})
            else:
                formatted_msgs.append(m)

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=formatted_msgs
        )
        return response.content[0].text

class LocalLLMClient(LLMClient):
    def __init__(self, host: str = "http://localhost:8000/v1/chat/completions"):
        self.host = host

    def generate(self, messages, temperature=0.7, max_tokens=512):
        payload = {
            "model": "llama-3-70b",
            "messages": messages,
            "temperature": temperature,
            "max_new_tokens": max_tokens
        }
        response = requests.post(self.host, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

class LLMEvaluator:
    """Evaluates factuality between RAG-generated answers and ground truth."""

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client


    # NEED TO ADJUST THE PROMPT RUBRIC
    def evaluate(self, question:str, generated: str, reference: str) -> str:
        """
        Compare the factuality between the generated and reference answers.
        Optionally include retrieved context to help LLM reasoning.
        """
        prompt = f"""
        You are an expert fact-checker. Compare the following two answers to the same question:

        Question: {question}
        Reference answer: {reference}
        Generated answer: {generated}

        Evaluate whether the generated answer is factually correct compared to the reference.
        Only consider factual accuracy, not style or completeness.

        Rate factual accuracy as one of the following:
        - "Correct" (All facts match the reference)
        - "Partially Correct" (Some but not all facts match)
        - "Incorrect" (Facts contradict or miss key points)

        Then explain your reasoning in 2-3 sentences.
        """

        messages = [
            {"role": "system", "content": "You are a careful factuality evaluator for RAG system."},
            {"role": "user", "content": prompt.strip()}
        ]

        return self.llm.generate(messages)