"""
LexiconTrail - Advanced Agentic AI System with NVIDIA SLMs and LlamaIndex

This is a demonstration package showing the architecture and design patterns
of LexiconTrail without revealing proprietary implementation details.
"""

from .client import LexiconTrailClient
from .mock_agents import DocumentAnalyzer, QueryProcessor, ResponseGenerator
from .exceptions import LexiconTrailError

__version__ = "1.0.0"
__author__ = "The AI Cowboys"
__email__ = "m_pendleton@theaicowboys.com"

__all__ = [
    "LexiconTrailClient",
    "DocumentAnalyzer",
    "QueryProcessor", 
    "ResponseGenerator",
    "LexiconTrailError"
]