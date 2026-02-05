"""Tests for CLI module"""

import pytest
import tempfile
import os
from click.testing import CliRunner
from hos.cli.main import cli


def test_cli_protect_command():
    """Test protect command"""
    runner = CliRunner()
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('print("Hello World")')
        input_file = f.name
    
    try:
        # Test with local provider (default)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            output_file = f.name
        
        result = runner.invoke(cli, [
            'protect',
            '--input', input_file,
            '--output', output_file,
            '--level', 'medium',
            '--mode', 'balanced'
        ])
        
        assert result.exit_code == 0
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
        
        # Clean up
        os.unlink(output_file)
        
    finally:
        os.unlink(input_file)


def test_cli_analyze_command():
    """Test analyze command"""
    runner = CliRunner()
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('def test():\n    return 42')
        input_file = f.name
    
    try:
        # Test analyze command
        result = runner.invoke(cli, [
            'analyze-cmd',
            '--file', input_file
        ])
        
        assert result.exit_code == 0
        assert '分析结果' in result.output
        assert '代码行数' in result.output
        assert '函数数量' in result.output
        
    finally:
        os.unlink(input_file)


def test_cli_version_command():
    """Test version command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['version'])
    assert result.exit_code == 0
    assert 'HOS-MAKE' in result.output


def test_cli_help_command():
    """Test help command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['help-cmd'])
    assert result.exit_code == 0
    assert 'HOS-MAKE - AI驱动的代码加密系统' in result.output


def test_cli_protect_with_provider_option():
    """Test protect command with provider option"""
    runner = CliRunner()
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('print("Test")')
        input_file = f.name
    
    try:
        # Test with different providers
        for provider in ['local']:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                output_file = f.name
            
            result = runner.invoke(cli, [
                'protect',
                '--input', input_file,
                '--output', output_file,
                '--level', 'low',
                '--mode', 'performance',
                '--provider', provider
            ])
            
            assert result.exit_code == 0
            assert os.path.exists(output_file)
            
            # Clean up
            os.unlink(output_file)
            
    finally:
        os.unlink(input_file)


def test_cli_error_handling():
    """Test CLI error handling"""
    runner = CliRunner()
    
    # Test with non-existent input file
    result = runner.invoke(cli, [
        'protect',
        '--input', 'non_existent_file.py',
        '--output', 'output.py'
    ])
    
    assert result.exit_code != 0
    assert '错误: 输入文件或目录' in result.output


def test_cli_directory_protection():
    """Test directory protection"""
    runner = CliRunner()
    
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as input_dir:
        # Create test file
        test_file = os.path.join(input_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write('print("Test")')
        
        # Create output directory
        with tempfile.TemporaryDirectory() as output_dir:
            result = runner.invoke(cli, [
                'protect',
                '--input', input_dir,
                '--output', output_dir,
                '--level', 'low'
            ])
            
            assert result.exit_code == 0
            assert '加密完成' in result.output
            
            # Check that output file was created
            output_file = os.path.join(output_dir, 'test.py')
            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0
