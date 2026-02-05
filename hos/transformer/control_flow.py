"""控制流变换模块"""

import random
import re

class ControlFlowTransformer:
    """控制流变换"""
    
    def __init__(self):
        """初始化控制流变换器"""
        self.loop_counter = 0
        self.if_counter = 0
    
    def transform(self, code, strategy):
        """应用控制流变换
        
        Args:
            code: 源代码字符串
            strategy: 混淆策略
            
        Returns:
            str: 变换后的代码
        """
        transformed_code = code
        
        # 应用控制流平坦化
        if strategy.control_flow.get('flattening', False):
            transformed_code = self._flatten_control_flow(transformed_code)
        
        # 应用伪分支
        if strategy.control_flow.get('fake_branches', False):
            transformed_code = self._add_fake_branches(transformed_code)
        
        # 应用异常驱动流
        if strategy.control_flow.get('exception_flow', False):
            transformed_code = self._add_exception_flow(transformed_code)
        
        # 应用循环变换
        if strategy.control_flow.get('loop_transform', False):
            transformed_code = self._transform_loops(transformed_code)
        
        return transformed_code
    
    def _flatten_control_flow(self, code):
        """控制流平坦化
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 寻找函数定义
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):\s*(.*?)(?=def|class|$)', re.DOTALL)
        
        def replace_function(match):
            function_name = match.group(1)
            params = match.group(2)
            body = match.group(3)
            
            # 生成平坦化后的函数体
            flattened_body = self._flatten_function_body(body)
            
            # 重建函数定义
            return f"def {function_name}({params}):\n{flattened_body}"
        
        return function_pattern.sub(replace_function, code)
    
    def _flatten_function_body(self, body):
        """平坦化函数体
        
        Args:
            body: 函数体代码
            
        Returns:
            str: 平坦化后的函数体
        """
        indent = self._get_indent(body)
        
        # 生成状态变量和跳转表
        state_var = f"_state_{random.randint(1000, 9999)}"
        jump_table_var = f"_jump_{random.randint(1000, 9999)}"
        
        # 分割代码块，考虑嵌套结构
        blocks = self._split_into_blocks(body)
        
        if not blocks:
            return body
        
        # 生成随机状态映射
        state_map = {}
        for i in range(len(blocks)):
            state_map[i] = random.randint(100, 999)
        
        # 生成跳转表
        jump_table = "{"
        for i, state in state_map.items():
            if i < len(blocks) - 1:
                next_state = state_map[i + 1]
            else:
                next_state = -1  # 终止状态
            jump_table += f"{state}: {next_state}, "
        jump_table = jump_table.rstrip(", ") + "}"
        
        # 生成平坦化代码
        flattened = []
        flattened.append(f"{indent}{jump_table_var} = {jump_table}")
        flattened.append(f"{indent}{state_var} = {state_map[0]}")
        flattened.append(f"{indent}while {state_var} != -1:")
        
        # 添加每个代码块
        for i, block in enumerate(blocks):
            state = state_map[i]
            flattened.append(f"{indent}    if {state_var} == {state}:")
            
            # 添加代码块内容
            block_lines = block.strip().split('\n')
            for line in block_lines:
                flattened.append(f"{indent}        {line}")
            
            # 添加状态转换
            if i < len(blocks) - 1:
                next_state = state_map[i + 1]
                flattened.append(f"{indent}        {state_var} = {next_state}")
            else:
                flattened.append(f"{indent}        {state_var} = -1")
        
        return '\n'.join(flattened)
    
    def _add_fake_branches(self, code):
        """添加伪分支
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 寻找if语句
        if_pattern = re.compile(r'(\s*)if\s+(.*?):\s*(.*?)(?=elif|else|def|class|$)', re.DOTALL)
        
        def replace_if(match):
            indent = match.group(1)
            condition = match.group(2)
            body = match.group(3)
            
            # 生成伪分支
            fake_var = f"_fake_{random.randint(1000, 9999)}"
            fake_condition = f"{fake_var} == {random.randint(1, 100)}"
            
            # 重建if语句，添加伪分支
            new_if = []
            new_if.append(f"{indent}{fake_var} = {random.randint(1, 100)}")
            new_if.append(f"{indent}if {condition} and not {fake_condition}:")
            new_if.append(body)
            new_if.append(f"{indent}elif {fake_condition}:")
            new_if.append(f"{indent}    pass  # 伪分支")
            new_if.append(f"{indent}else:")
            new_if.append(f"{indent}    pass")
            
            return '\n'.join(new_if)
        
        return if_pattern.sub(replace_if, code)
    
    def _add_exception_flow(self, code):
        """添加异常驱动流
        
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
            
            # 生成异常驱动的函数体
            exception_body = self._add_exception_handlers(body)
            
            # 重建函数定义
            return f"def {function_name}({params}):\n{exception_body}"
        
        return function_pattern.sub(replace_function, code)
    
    def _add_exception_handlers(self, body):
        """添加异常处理器
        
        Args:
            body: 函数体代码
            
        Returns:
            str: 变换后的函数体
        """
        # 简化版实现
        indent = self._get_indent(body)
        
        # 生成异常类名
        exception_name = f"_FakeException_{random.randint(1000, 9999)}"
        
        # 生成异常驱动代码
        exception_code = []
        exception_code.append(f"{indent}class {exception_name}(Exception):")
        exception_code.append(f"{indent}    pass")
        exception_code.append("")
        exception_code.append(f"{indent}try:")
        
        # 添加原始代码
        body_lines = body.strip().split('\n')
        for line in body_lines:
            exception_code.append(f"{indent}    {line}")
        
        # 添加异常处理器
        exception_code.append(f"{indent}except {exception_name}:")
        exception_code.append(f"{indent}    pass")
        exception_code.append(f"{indent}except Exception:")
        exception_code.append(f"{indent}    raise")
        
        return '\n'.join(exception_code)
    
    def _transform_loops(self, code):
        """变换循环
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 寻找for循环
        for_pattern = re.compile(r'(\s*)for\s+(.*?)\s+in\s+(.*?):\s*(.*?)(?=for|while|if|def|class|$)', re.DOTALL)
        
        def replace_for(match):
            indent = match.group(1)
            var = match.group(2)
            iterable = match.group(3)
            body = match.group(4)
            
            # 生成变换后的循环
            transformed_for = self._transform_for_loop(indent, var, iterable, body)
            
            return transformed_for
        
        # 应用for循环变换
        code = for_pattern.sub(replace_for, code)
        
        # 寻找while循环
        while_pattern = re.compile(r'(\s*)while\s+(.*?):\s*(.*?)(?=for|while|if|def|class|$)', re.DOTALL)
        
        def replace_while(match):
            indent = match.group(1)
            condition = match.group(2)
            body = match.group(3)
            
            # 生成变换后的循环
            transformed_while = self._transform_while_loop(indent, condition, body)
            
            return transformed_while
        
        return while_pattern.sub(replace_while, code)
    
    def _transform_for_loop(self, indent, var, iterable, body):
        """变换for循环
        
        Args:
            indent: 缩进
            var: 循环变量
            iterable: 可迭代对象
            body: 循环体
            
        Returns:
            str: 变换后的循环
        """
        # 生成迭代器变量
        iter_var = f"_iter_{random.randint(1000, 9999)}"
        
        # 生成变换后的循环
        transformed = []
        transformed.append(f"{indent}{iter_var} = iter({iterable})")
        transformed.append(f"{indent}while True:")
        transformed.append(f"{indent}    try:")
        transformed.append(f"{indent}        {var} = next({iter_var})")
        transformed.append(body)
        transformed.append(f"{indent}    except StopIteration:")
        transformed.append(f"{indent}        break")
        
        return '\n'.join(transformed)
    
    def _transform_while_loop(self, indent, condition, body):
        """变换while循环
        
        Args:
            indent: 缩进
            condition: 循环条件
            body: 循环体
            
        Returns:
            str: 变换后的循环
        """
        # 生成状态变量
        state_var = f"_state_{random.randint(1000, 9999)}"
        
        # 生成变换后的循环
        transformed = []
        transformed.append(f"{indent}{state_var} = True")
        transformed.append(f"{indent}while {state_var}:")
        transformed.append(f"{indent}    if not ({condition}):")
        transformed.append(f"{indent}        {state_var} = False")
        transformed.append(f"{indent}    else:")
        transformed.append(body)
        
        return '\n'.join(transformed)
    
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
    
    def _split_into_blocks(self, code):
        """将代码分割成块
        
        Args:
            code: 代码字符串
            
        Returns:
            list: 代码块列表
        """
        lines = code.strip().split('\n')
        blocks = []
        current_block = []
        indent_level = 0
        in_block = False
        
        for line in lines:
            stripped_line = line.strip()
            
            if not stripped_line:
                if current_block and in_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
                    in_block = False
                continue
            
            # 计算当前行的缩进级别
            line_indent = len(line) - len(stripped_line)
            
            # 检查是否是块的开始
            if any(stripped_line.endswith(char) for char in [':', '{', '[', '(']) and not stripped_line.endswith('\\\\'):
                if current_block and in_block and line_indent <= indent_level:
                    blocks.append('\n'.join(current_block))
                    current_block = []
                current_block.append(line)
                indent_level = line_indent
                in_block = True
            elif stripped_line.startswith('return') or stripped_line.startswith('raise'):
                # 单独处理返回和异常语句
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
                blocks.append(line)
                in_block = False
            else:
                current_block.append(line)
                in_block = True
        
        if current_block:
            blocks.append('\n'.join(current_block))
        
        return blocks
