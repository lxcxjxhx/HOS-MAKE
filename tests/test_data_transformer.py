"""Tests for data transformer"""

import pytest
from hos.transformer.data import DataTransformer
from hos.ai.strategy import ConfusionStrategy


def test_data_transformer_initialization():
    """Test data transformer initialization"""
    transformer = DataTransformer()
    assert transformer is not None


def test_constant_splitting():
    """Test constant splitting"""
    transformer = DataTransformer()
    code = "x = 12345"
    
    strategy = ConfusionStrategy()
    strategy.data['constant_splitting'] = True
    
    transformed = transformer.transform(code, strategy)
    assert "12345" not in transformed
    assert "_const_" in transformed


def test_dynamic_calculation():
    """Test dynamic calculation"""
    transformer = DataTransformer()
    code = "x = 42"
    
    strategy = ConfusionStrategy()
    strategy.data['dynamic_calculation'] = True
    
    transformed = transformer.transform(code, strategy)
    assert "42" not in transformed
    # Check that the expression is more complex than just the number
    assert len(transformed) > len(code)


def test_string_encryption():
    """Test string encryption"""
    transformer = DataTransformer()
    code = 'print("Hello World")'
    
    strategy = ConfusionStrategy()
    strategy.data['string_encryption'] = True
    
    transformed = transformer.transform(code, strategy)
    assert '"Hello World"' not in transformed
    assert "_str_" in transformed
    # The decrypt function is added at the beginning of the code
    assert "def _decrypt_" in transformed


def test_encoding_table():
    """Test encoding table"""
    transformer = DataTransformer()
    code = "x = 1"
    
    strategy = ConfusionStrategy()
    strategy.data['encoding_table'] = True
    
    transformed = transformer.transform(code, strategy)
    assert "_encoding_table_" in transformed
    assert "_decode_" in transformed


def test_polymorphic_encoding():
    """Test polymorphic encoding"""
    transformer = DataTransformer()
    code = "x = 1"
    
    strategy = ConfusionStrategy()
    strategy.data['polymorphic_encoding'] = True
    
    transformed = transformer.transform(code, strategy)
    assert "_encode_" in transformed
    assert "_decode_" in transformed


def test_combined_transformations():
    """Test combined transformations"""
    transformer = DataTransformer()
    code = 'x = 12345\nprint("Hello")'
    
    strategy = ConfusionStrategy()
    strategy.data['constant_splitting'] = True
    strategy.data['dynamic_calculation'] = True
    strategy.data['string_encryption'] = True
    strategy.data['encoding_table'] = True
    strategy.data['polymorphic_encoding'] = True
    
    transformed = transformer.transform(code, strategy)
    assert "12345" not in transformed
    assert '"Hello"' not in transformed
    assert "_const_" in transformed
    assert "_str_" in transformed
    assert "_decode_" in transformed


def test_transform_without_strategy():
    """Test transformation without strategy"""
    transformer = DataTransformer()
    code = "x = 1"
    
    strategy = ConfusionStrategy()
    # All data transformations disabled
    
    transformed = transformer.transform(code, strategy)
    assert transformed == code


def test_edge_cases():
    """Test edge cases"""
    transformer = DataTransformer()
    
    # Test empty code
    strategy = ConfusionStrategy()
    strategy.data['string_encryption'] = True
    
    empty_result = transformer.transform("", strategy)
    assert empty_result == ""
    
    # Test code without strings
    no_strings = "x = 1\ny = 2"
    strategy.data['string_encryption'] = True
    result = transformer.transform(no_strings, strategy)
    assert result == no_strings
    
    # Test code without constants
    no_constants = 'x = input()\nprint(x)'
    strategy.data['constant_splitting'] = True
    result = transformer.transform(no_constants, strategy)
    assert result == no_constants
