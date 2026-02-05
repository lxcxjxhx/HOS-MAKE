"""Tests for AI providers"""

import pytest
from hos.ai.providers import AIProviderFactory
from hos.ai.providers.local import LocalProvider


def test_provider_factory():
    """Test AI provider factory"""
    # Test that local provider is always available
    local_provider = AIProviderFactory.create_provider('local')
    assert local_provider.is_available() is True
    assert local_provider.get_name() == 'LocalProvider'


def test_local_provider():
    """Test local provider functionality"""
    provider = LocalProvider()
    assert provider.is_available() is True
    
    # Test strategy generation
    code_analysis = {
        'code_size': 1000,
        'line_count': 50,
        'ast': {
            'functions': [{'name': 'test'}],
            'classes': []
        },
        'hot_paths': [],
        'sensitivity': {'sensitivity_score': 50},
        'security_score': 50
    }
    
    # Test different performance modes
    for mode in ['balanced', 'performance', 'security']:
        strategy = provider.generate_strategy(code_analysis, mode)
        assert isinstance(strategy, dict)
        assert 'control_flow' in strategy
        assert 'data' in strategy
        assert 'instruction' in strategy
        assert 'structure' in strategy
        assert 'virtualization' in strategy
        assert 'performance' in strategy


def test_provider_error_handling():
    """Test provider error handling"""
    # Test with invalid provider name
    with pytest.raises(ValueError):
        AIProviderFactory.create_provider('invalid_provider')


def test_strategy_generation_fallback():
    """Test strategy generation fallback"""
    # Test with minimal code analysis
    provider = LocalProvider()
    strategy = provider.generate_strategy(None, 'balanced')
    assert isinstance(strategy, dict)
    assert 'control_flow' in strategy


def test_provider_configuration():
    """Test provider configuration"""
    # Test with custom configuration
    config = {'random_seed': 42}
    provider = LocalProvider(config=config)
    assert provider.is_available() is True
    
    # Test strategy generation with config
    strategy1 = provider.generate_strategy(None, 'balanced')
    strategy2 = provider.generate_strategy(None, 'balanced')
    # With the same seed, strategies should be similar
    assert strategy1['control_flow']['flattening'] == strategy2['control_flow']['flattening']
