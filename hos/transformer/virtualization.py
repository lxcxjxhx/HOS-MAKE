"""虚拟化变换模块"""

import random
import re

class VirtualizationTransformer:
    """虚拟化变换"""
    
    def __init__(self):
        """初始化虚拟化变换器"""
        self.vm_counter = 0
    
    def transform(self, code, strategy):
        """应用虚拟化变换
        
        Args:
            code: 源代码字符串
            strategy: 混淆策略
            
        Returns:
            str: 变换后的代码
        """
        transformed_code = code
        
        # 应用虚拟化
        if strategy.virtualization.get('enabled', False):
            # 检查是否启用字节码VM
            if strategy.virtualization.get('bytecode_vm', False):
                transformed_code = self._virtualize_with_bytecode(transformed_code)
            
            # 检查是否启用解释执行
            if strategy.virtualization.get('interpreted_execution', False):
                transformed_code = self._virtualize_with_interpretation(transformed_code)
        
        return transformed_code
    
    def _virtualize_with_bytecode(self, code):
        """使用字节码VM虚拟化
        
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
            
            # 虚拟化函数
            virtualized_function = self._virtualize_function(function_name, params, body)
            
            return virtualized_function
        
        # 添加VM解释器
        vm_interpreter = self._generate_vm_interpreter()
        code = vm_interpreter + '\n\n' + code
        
        return function_pattern.sub(replace_function, code)
    
    def _virtualize_function(self, function_name, params, body):
        """虚拟化单个函数
        
        Args:
            function_name: 函数名
            params: 函数参数
            body: 函数体
            
        Returns:
            str: 虚拟化后的函数代码
        """
        # 生成字节码
        bytecode = self._generate_bytecode(body)
        
        # 生成虚拟化函数
        vm_name = f"vm_{random.randint(1000, 9999)}"
        bytecode_var = f"_bytecode_{random.randint(1000, 9999)}"
        
        # 生成函数代码
        function_code = f"def {function_name}({params}):\n"
        function_code += f"    {bytecode_var} = {bytecode}\n"
        function_code += f"    return {vm_name}({bytecode_var}, locals())"
        
        return function_code
    
    def _generate_bytecode(self, body):
        """生成字节码
        
        Args:
            body: 函数体代码
            
        Returns:
            str: 字节码列表的字符串表示
        """
        # 简化版实现，将代码转换为字节码指令
        instructions = []
        
        # 分割代码行
        lines = body.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # 生成指令
            instruction = self._generate_instruction(line)
            instructions.append(instruction)
        
        return str(instructions)
    
    def _generate_instruction(self, line):
        """生成单个指令
        
        Args:
            line: 代码行
            
        Returns:
            dict: 指令字典
        """
        # 简化版实现
        if '=' in line:
            # 赋值指令
            parts = line.split('=', 1)
            var = parts[0].strip()
            expr = parts[1].strip()
            return {'op': 'SET', 'args': [var, expr]}
        elif 'return' in line:
            # 返回指令
            parts = line.split('return', 1)
            if len(parts) > 1:
                expr = parts[1].strip()
                return {'op': 'RETURN', 'args': [expr]}
            else:
                return {'op': 'RETURN', 'args': []}
        elif 'if' in line:
            # 条件指令
            parts = line.split('if', 1)
            if len(parts) > 1:
                cond = parts[1].strip().rstrip(':')
                return {'op': 'IF', 'args': [cond]}
        elif 'for' in line:
            # 循环指令
            parts = line.split('for', 1)
            if len(parts) > 1:
                loop = parts[1].strip().rstrip(':')
                return {'op': 'FOR', 'args': [loop]}
        elif 'while' in line:
            # 循环指令
            parts = line.split('while', 1)
            if len(parts) > 1:
                cond = parts[1].strip().rstrip(':')
                return {'op': 'WHILE', 'args': [cond]}
        
        # 默认指令
        return {'op': 'EXEC', 'args': [line]}
    
    def _generate_vm_interpreter(self):
        """生成VM解释器
        
        Returns:
            str: VM解释器代码
        """
        vm_name = f"vm_{random.randint(1000, 9999)}"
        
        interpreter_code = f"def {vm_name}(bytecode, context):\n"
        interpreter_code += f"    stack = []\n"
        interpreter_code += f"    pc = 0\n"
        interpreter_code += f"    while pc < len(bytecode):\n"
        interpreter_code += f"        instr = bytecode[pc]\n"
        interpreter_code += f"        op = instr['op']\n"
        interpreter_code += f"        args = instr.get('args', [])\n"
        interpreter_code += f"        if op == 'SET':\n"
        interpreter_code += f"            var = args[0]\n"
        interpreter_code += f"            expr = args[1]\n"
        interpreter_code += f"            context[var] = eval(expr, globals(), context)\n"
        interpreter_code += f"        elif op == 'RETURN':\n"
        interpreter_code += f"            if args:\n"
        interpreter_code += f"                return eval(args[0], globals(), context)\n"
        interpreter_code += f"            else:\n"
        interpreter_code += f"                return None\n"
        interpreter_code += f"        elif op == 'IF':\n"
        interpreter_code += f"            cond = args[0]\n"
        interpreter_code += f"            if not eval(cond, globals(), context):\n"
        interpreter_code += f"                # 跳过下一条指令\n"
        interpreter_code += f"                pc += 1\n"
        interpreter_code += f"        elif op == 'EXEC':\n"
        interpreter_code += f"            exec(args[0], globals(), context)\n"
        interpreter_code += f"        pc += 1\n"
        interpreter_code += f"    return None"
        
        return interpreter_code
    
    def _virtualize_with_interpretation(self, code):
        """使用解释执行虚拟化
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 生成解释器
        interpreter = self._generate_interpreter()
        
        # 包装代码
        wrapped_code = self._wrap_code_with_interpreter(code, interpreter)
        
        return wrapped_code
    
    def _generate_interpreter(self):
        """生成解释器
        
        Returns:
            str: 解释器代码
        """
        interpreter_name = f"interpret_{random.randint(1000, 9999)}"
        
        interpreter_code = f"def {interpreter_name}(code, context=None):\n"
        interpreter_code += f"    if context is None:\n"
        interpreter_code += f"        context = {{}}\n"
        interpreter_code += f"    # 简单的解释器实现\n"
        interpreter_code += f"    lines = code.strip().split('\\n')\n"
        interpreter_code += f"    for line in lines:\n"
        interpreter_code += f"        line = line.strip()\n"
        interpreter_code += f"        if not line or line.startswith('#'):\n"
        interpreter_code += f"            continue\n"
        interpreter_code += f"        exec(line, globals(), context)\n"
        interpreter_code += f"    return context"
        
        return interpreter_code
    
    def _wrap_code_with_interpreter(self, code, interpreter):
        """使用解释器包装代码
        
        Args:
            code: 源代码字符串
            interpreter: 解释器代码
            
        Returns:
            str: 包装后的代码
        """
        # 提取解释器名
        interpreter_name_match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', interpreter)
        if not interpreter_name_match:
            return code
        
        interpreter_name = interpreter_name_match.group(1)
        
        # 包装代码
        wrapped_code = interpreter + '\n\n'
        wrapped_code += f"# 原始代码被解释执行\n"
        wrapped_code += f"_code = '''{code}'''\n"
        wrapped_code += f"_context = {interpreter_name}(_code)\n"
        
        return wrapped_code
