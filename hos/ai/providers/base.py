"""Base AI provider classes"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize AI provider
        
        Args:
            api_key: API key for the provider
            config: Additional configuration parameters
        """
        self.api_key = api_key
        self.config = config or {}
        self.provider_name = self.__class__.__name__
    
    @abstractmethod
    def generate_strategy(self, code_analysis: Dict[str, Any], performance_mode: str = 'balanced') -> Dict[str, Any]:
        """Generate confusion strategy using AI
        
        Args:
            code_analysis: Code analysis results
            performance_mode: Performance mode ('balanced', 'performance', 'security')
            
        Returns:
            Dict[str, Any]: Generated strategy configuration
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available
        
        Returns:
            bool: True if provider is available, False otherwise
        """
        pass
    
    def get_name(self) -> str:
        """Get provider name
        
        Returns:
            str: Provider name
        """
        return self.provider_name


class AIProviderFactory:
    """Factory for creating AI provider instances"""
    
    _providers = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """Register a new AI provider
        
        Args:
            name: Provider name
            provider_class: Provider class
        """
        cls._providers[name] = provider_class
    
    @classmethod
    def create_provider(cls, name: str, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> AIProvider:
        """Create AI provider instance
        
        Args:
            name: Provider name
            api_key: API key
            config: Additional configuration
            
        Returns:
            AIProvider: Provider instance
            
        Raises:
            ValueError: If provider name is not registered
        """
        if name not in cls._providers:
            raise ValueError(f"Unknown AI provider: {name}")
        
        return cls._providers[name](api_key, config)
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Get list of available providers
        
        Returns:
            list: Available provider names
        """
        return list(cls._providers.keys())
