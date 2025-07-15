"""
Custom exceptions for LexiconTrail
"""


class LexiconTrailError(Exception):
    """Base exception for LexiconTrail"""
    pass


class AgentError(LexiconTrailError):
    """Error in agent processing"""
    pass


class ConfigurationError(LexiconTrailError):
    """Configuration related errors"""
    pass


class AuthenticationError(LexiconTrailError):
    """Authentication failures"""
    pass


class RateLimitError(LexiconTrailError):
    """Rate limit exceeded"""
    pass


class TimeoutError(LexiconTrailError):
    """Operation timeout"""
    pass