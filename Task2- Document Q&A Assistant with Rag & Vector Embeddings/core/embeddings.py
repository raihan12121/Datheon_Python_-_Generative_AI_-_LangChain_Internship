"""
Embeddings generation module supporting Local ONNX (Chroma default), Google Gemini, and OpenAI.
"""

import os
import logging
from typing import List, Optional
from langchain_core.embeddings import Embeddings
import chromadb.utils.embedding_functions as ef
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("RAGEmbeddings")


class LocalChromaEmbeddings(Embeddings):
    """
    Local dense embedding generator using Chroma's default all-MiniLM-L6-v2 ONNX model.
    Runs 100% offline, highly performant, and requires zero external API keys.
    """

    def __init__(self):
        self._ef = ef.DefaultEmbeddingFunction()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._ef(texts)

    def embed_query(self, text: str) -> List[float]:
        results = self._ef([text])
        return results[0] if results else []


class GeminiEmbeddings(Embeddings):
    """Embeddings generator using Google Gemini API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "models/text-embedding-004"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model = model
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for GeminiEmbeddings.")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            result = client.models.embed_content(
                model=self.model,
                contents=texts,
            )
            return [e.values for e in result.embeddings]
        except Exception as e:
            logger.warning(f"Failed to use google.genai: {e}. Falling back to local embeddings.")
            return LocalChromaEmbeddings().embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            result = client.models.embed_content(
                model=self.model,
                contents=text,
            )
            return result.embeddings[0].values
        except Exception:
            return LocalChromaEmbeddings().embed_query(text)


class OpenAIEmbeddingsModel(Embeddings):
    """Embeddings generator using OpenAI API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAIEmbeddings.")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        resp = client.embeddings.create(input=texts, model=self.model)
        return [item.embedding for item in resp.data]

    def embed_query(self, text: str) -> List[float]:
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        resp = client.embeddings.create(input=[text], model=self.model)
        return resp.data[0].embedding


def get_embeddings_generator(provider: Optional[str] = None) -> Embeddings:
    """Factory selecting the embedding provider based on environment and availability."""
    prov = (provider or os.getenv("DEFAULT_LLM_PROVIDER") or "local").lower()

    if prov == "gemini" and (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        try:
            return GeminiEmbeddings()
        except Exception as e:
            logger.warning(f"Could not initialize Gemini embeddings ({e}). Using LocalChromaEmbeddings.")
            return LocalChromaEmbeddings()

    elif prov == "openai" and os.getenv("OPENAI_API_KEY"):
        try:
            return OpenAIEmbeddingsModel()
        except Exception as e:
            logger.warning(f"Could not initialize OpenAI embeddings ({e}). Using LocalChromaEmbeddings.")
            return LocalChromaEmbeddings()

    return LocalChromaEmbeddings()
