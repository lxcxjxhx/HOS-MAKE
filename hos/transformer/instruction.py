"""指令级变换模块"""

import random
import re

class InstructionTransformer:
    """指令级变换"""
    
    def __init__(self):
        """初始化指令级变换器"""
        self.inject_counter = 0
        self.subst_counter = 0
    
    def transform(self, code, strategy):
        """应用指令级变换
        
        Args:
            code: 源代码字符串
            strategy: 混淆策略
            
        Returns:
            str: 变换后的代码
        """
        transformed_code = code
        
        # 应用垃圾指令注入
        if strategy.instruction.get('garbage_injection', False):
            transformed_code = self._inject_garbage_instructions(transformed_code)
        
        # 应用等价指令替换
        if strategy.instruction.get('instruction_substitution', False):
            transformed_code = self._substitute_instructions(transformed_code)
        
        # 应用寄存器分配混淆
        if strategy.instruction.get('register_allocation', False):
            transformed_code = self._obfuscate_register_allocation(transformed_code)
        
        return transformed_code
    
    def _inject_garbage_instructions(self, code):
        """注入垃圾指令
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 寻找函数定义
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):\s*(.*?)(?=def|$)', re.DOTALL)
        
        def replace_function(match):
            function_name = match.group(1)
            params = match.group(2)
            body = match.group(3)
            
            # 注入垃圾指令
            injected_body = self._inject_garbage_into_body(body)
            
            # 重建函数定义
            return f"def {function_name}({params}):\n{injected_body}"
        
        return function_pattern.sub(replace_function, code)
    
    def _inject_garbage_into_body(self, body):
        """向函数体注入垃圾指令
        
        Args:
            body: 函数体代码
            
        Returns:
            str: 注入后的函数体
        """
        lines = body.strip().split('\n')
        if not lines:
            return body
        
        # 获取缩进
        indent = self._get_indent(body)
        
        # 生成垃圾指令
        garbage_instructions = self._generate_garbage_instructions(indent)
        
        # 注入垃圾指令
        injected_lines = []
        for i, line in enumerate(lines):
            injected_lines.append(line)
            
            # 每3行注入一次垃圾指令
            if (i + 1) % 3 == 0:
                injected_lines.extend(garbage_instructions)
        
        return '\n'.join(injected_lines)
    
    def _generate_garbage_instructions(self, indent):
        """生成垃圾指令
        
        Args:
            indent: 缩进
            
        Returns:
            list: 垃圾指令列表
        """
        garbage = []
        
        # 生成随机垃圾指令
        garbage_types = [
            self._generate_useless_calculation,
            self._generate_useless_assignment,
            self._generate_useless_condition,
            self._generate_useless_loop
        ]
        
        # 随机选择2-4条垃圾指令
        num_instructions = random.randint(2, 4)
        for _ in range(num_instructions):
            gen_func = random.choice(garbage_types)
            instruction = gen_func(indent)
            garbage.append(instruction)
        
        return garbage
    
    def _generate_useless_calculation(self, indent):
        """生成无用的计算
        
        Args:
            indent: 缩进
            
        Returns:
            str: 无用计算指令
        """
        var1 = f"_garbage_{random.randint(1000, 9999)}"
        var2 = f"_garbage_{random.randint(1000, 9999)}"
        
        # 生成随机计算
        op1 = random.randint(1, 100)
        op2 = random.randint(1, 100)
        op = random.choice(['+', '-', '*', '/'])
        
        return f"{indent}{var1} = {op1} {op} {op2}\n{indent}{var2} = {var1} % 10"
    
    def _generate_useless_assignment(self, indent):
        """生成无用的赋值
        
        Args:
            indent: 缩进
            
        Returns:
            str: 无用赋值指令
        """
        var = f"_garbage_{random.randint(1000, 9999)}"
        values = [
            random.randint(1, 100),
            random.choice(['True', 'False', 'None']),
            f"'{'x' * random.randint(1, 10)}'",
            '[]',
            '{}',
            '()'
        ]
        value = random.choice(values)
        
        return f"{indent}{var} = {value}"
    
    def _generate_useless_condition(self, indent):
        """生成无用的条件
        
        Args:
            indent: 缩进
            
        Returns:
            str: 无用条件指令
        """
        var = f"_garbage_{random.randint(1000, 9999)}"
        cond = random.choice([
            f"{var} == 0",
            f"{var} is not None",
            f"len({var}) > 0",
            "True",
            "False"
        ])
        
        return f"{indent}{var} = False\n{indent}if {cond}:\n{indent}    pass"
    
    def _generate_useless_loop(self, indent):
        """生成无用的循环
        
        Args:
            indent: 缩进
            
        Returns:
            str: 无用循环指令
        """
        var = f"_garbage_{random.randint(1000, 9999)}"
        limit = random.randint(1, 5)
        
        return f"{indent}for {var} in range({limit}):\n{indent}    pass"
    
    def _substitute_instructions(self, code):
        """替换等价指令
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 替换常见的指令为等价形式
        substitutions = [
            # 替换 True/False
            (r'\bTrue\b', 'not False'),
            (r'\bFalse\b', 'not True'),
            
            # 替换空容器
            (r'\[\s*\]', 'list()'),
            (r'\{\s*\}', 'dict()'),
            (r'\(\s*\)', 'tuple()'),
            
            # 替换算术操作
            (r'(\d+)\s*\+\s*(\d+)', r'((\1) + (\2))'),
            (r'(\d+)\s*\*\s*(\d+)', r'((\1) * (\2))'),
            
            # 替换比较操作
            (r'(\w+)\s*==\s*(\w+)', r'not ((\1) != (\2))'),
            (r'(\w+)\s*!=\s*(\w+)', r'not ((\1) == (\2))'),
            (r'(\w+)\s*>\s*(\w+)', r'not ((\1) <= (\2))'),
            (r'(\w+)\s*<\s*(\w+)', r'not ((\1) >= (\2))'),
        ]
        
        # 应用替换
        for pattern, replacement in substitutions:
            code = re.sub(pattern, replacement, code)
        
        return code
    
    def _obfuscate_register_allocation(self, code):
        """混淆寄存器分配
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 寻找变量名
        var_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b')
        
        # 收集所有变量名
        vars = set()
        for match in var_pattern.finditer(code):
            var = match.group(1)
            # 跳过内置函数和关键字
            if var not in ['def', 'class', 'if', 'else', 'for', 'while', 'return', 'pass', 'import', 'from']:
                vars.add(var)
        
        # 生成变量映射
        var_map = {}
        for var in vars:
            if not var.startswith('_'):
                var_map[var] = f"_reg_{random.randint(1000, 9999)}"
        
        # 替换变量名
        obfuscated_code = code
        for old_var, new_var in var_map.items():
            # 使用边界匹配确保只替换完整的变量名
            pattern = rf'\b{old_var}\b'
            obfuscated_code = re.sub(pattern, new_var, obfuscated_code)
        
        return obfuscated_code
    
    def _get_indent(self, code):
        """获取代码的缩进
        
        Args:
            code: 代码字符串
            
        Returns:
            str: 缩进字符串
        """
        lines = code.strip().split('\n')
        if not lines:
            return ''
        
        first_line = lines[0]
        indent = ''
        for char in first_line:
            if char in (' ', '\t'):
                indent += char
            else:
                break
        
        return indent
