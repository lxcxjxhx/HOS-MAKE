"""Integration tests for end-to-end workflow"""

import pytest
import tempfile
import os
import subprocess


def test_end_to_end_protection():
    """Test end-to-end code protection workflow"""
    # Create a test Python file
    test_code = '''
def greet():
    return "Hello, World!"

def calculate(x, y):
    return x + y

if __name__ == "__main__":
    print(greet())
    print(calculate(5, 3))
'''
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create input file
        input_file = os.path.join(tmpdir, 'test.py')
        with open(input_file, 'w') as f:
            f.write(test_code)
        
        # Create output directory
        output_dir = os.path.join(tmpdir, 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Run HOS protection
        output_file = os.path.join(output_dir, 'test.py')
        result = subprocess.run(
            ['python', '-m', 'hos.cli.main', 'protect',
             '--input', input_file,
             '--output', output_file,
             '--level', 'medium',
             '--mode', 'balanced',
             '--provider', 'local'],
            capture_output=True,
            text=True
        )
        
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        print(f"Expected output file: {output_file}")
        print(f"Output file exists: {os.path.exists(output_file)}")
        
        assert result.returncode == 0
        assert '加密完成' in result.stdout
        
        # Check that output file was created
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
        
        # Verify the transformed code is different
        with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
            transformed_code = f.read()
        
        assert transformed_code != test_code
        assert 'Hello, World!' not in transformed_code
        assert 'greet' in transformed_code
        assert 'calculate' in transformed_code


def test_directory_protection():
    """Test directory protection workflow"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create input directory with multiple files
        input_dir = os.path.join(tmpdir, 'input')
        os.makedirs(input_dir, exist_ok=True)
        
        # Create test files
        files = {
            'test1.py': 'print("Test 1")',
            'test2.py': 'print("Test 2")',
            'subdir': {
                'test3.py': 'print("Test 3")'
            }
        }
        
        # Create files
        for name, content in files.items():
            if isinstance(content, dict):
                subdir = os.path.join(input_dir, name)
                os.makedirs(subdir, exist_ok=True)
                for subname, subcontent in content.items():
                    with open(os.path.join(subdir, subname), 'w') as f:
                        f.write(subcontent)
            else:
                with open(os.path.join(input_dir, name), 'w') as f:
                    f.write(content)
        
        # Create output directory
        output_dir = os.path.join(tmpdir, 'output')
        
        # Run HOS protection on directory
        result = subprocess.run(
            ['python', '-m', 'hos.cli.main', 'protect',
             '--input', input_dir,
             '--output', output_dir,
             '--level', 'low',
             '--mode', 'performance'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert '加密完成' in result.stdout
        
        # Check that all files were processed
        expected_files = [
            'test1.py',
            'test2.py',
            'subdir/test3.py'
        ]
        
        for expected_file in expected_files:
            output_file = os.path.join(output_dir, expected_file)
            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0


def test_analysis_workflow():
    """Test code analysis workflow"""
    test_code = '''
def complex_function(x, y):
    if x > y:
        return x * 2
    else:
        return y // 2
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        input_file = f.name
    
    try:
        # Run HOS analysis
        result = subprocess.run(
            ['python', '-m', 'hos.cli.main', 'analyze-cmd',
             '--file', input_file],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert '分析结果' in result.stdout
        assert '代码行数' in result.stdout
        assert '函数数量' in result.stdout
        assert '类数量' in result.stdout
        
    finally:
        os.unlink(input_file)


def test_performance_modes():
    """Test different performance modes"""
    test_code = 'x = 12345'
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create input file
        input_file = os.path.join(tmpdir, 'test.py')
        with open(input_file, 'w') as f:
            f.write(test_code)
        
        # Test different modes
        for mode in ['performance', 'balanced', 'security']:
            output_file = os.path.join(tmpdir, f'test_{mode}.py')
            
            # Run HOS protection
            result = subprocess.run(
                ['python', '-m', 'hos.cli.main', 'protect',
                 '--input', input_file,
                 '--output', output_file,
                 '--level', 'medium',
                 '--mode', mode],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0


def test_strength_levels():
    """Test different strength levels"""
    test_code = 'print("Hello")'
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create input file
        input_file = os.path.join(tmpdir, 'test.py')
        with open(input_file, 'w') as f:
            f.write(test_code)
        
        # Test different strength levels
        for level in ['low', 'medium', 'high']:
            output_file = os.path.join(tmpdir, f'test_{level}.py')
            
            # Run HOS protection
            result = subprocess.run(
                ['python', '-m', 'hos.cli.main', 'protect',
                 '--input', input_file,
                 '--output', output_file,
                 '--level', level,
                 '--mode', 'balanced'],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0


def test_edge_cases():
    """Test edge cases for Python obfuscation"""
    # Test edge cases
    edge_cases = [
        # Empty function
        ('''
def empty_function():
    pass
''', "empty_function"),
        
        # Function with only return
        ('''
def return_only():
    return 42
''', "return_only"),
        
        # Nested loops and conditionals
        ('''
def nested_structures():
    result = 0
    for i in range(5):
        if i > 2:
            for j in range(3):
                if j % 2 == 0:
                    result += i * j
    return result
''', "nested_structures"),
        
        # String manipulation
        ('''
def string_ops():
    s = "Hello, World!"
    return s.upper() + " " + s.lower()
''', "string_ops"),
        
        # Exception handling
        ('''
def exception_handling():
    try:
        return 10 / 0
    except ZeroDivisionError:
        return 0
''', "exception_handling"),
        
        # Lambda function
        ('''
def lambda_function():
    add = lambda x, y: x + y
    return add(5, 3)
''', "lambda_function"),
        
        # Generator expression
        ('''
def generator_expr():
    return sum(x * 2 for x in range(10) if x % 2 == 0)
''', "generator_expr"),
        
        # List comprehension
        ('''
def list_comp():
    return [x * 3 for x in range(5) if x > 0]
''', "list_comp"),
        
        # Dictionary comprehension
        ('''
def dict_comp():
    return {x: x * x for x in range(5)}
''', "dict_comp"),
        
        # Set comprehension
        ('''
def set_comp():
    return {x * 2 for x in range(10) if x % 2 == 0}
''', "set_comp"),
    ]
    
    for test_code, function_name in edge_cases:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create input file
            input_file = os.path.join(tmpdir, 'test.py')
            with open(input_file, 'w') as f:
                f.write(test_code)
            
            # Create output file
            output_file = os.path.join(tmpdir, 'test_protected.py')
            
            # Run HOS protection
            result = subprocess.run(
                ['python', '-m', 'hos.cli.main', 'protect',
                 '--input', input_file,
                 '--output', output_file,
                 '--level', 'medium',
                 '--mode', 'balanced'],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0
            
            # Read protected code
            with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                protected_code = f.read()
            
            # Verify obfuscation
            assert protected_code != test_code
            assert function_name in protected_code
