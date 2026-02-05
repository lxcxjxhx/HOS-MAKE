"""结构级变换模块"""

import random
import re

class StructureTransformer:
    """结构级变换"""
    
    def __init__(self):
        """初始化结构级变换器"""
        self.split_counter = 0
        self.merge_counter = 0
    
    def transform(self, code, strategy):
        """应用结构级变换
        
        Args:
            code: 源代码字符串
            strategy: 混淆策略
            
        Returns:
            str: 变换后的代码
        """
        transformed_code = code
        
        # 应用函数拆分
        if strategy.structure.get('function_splitting', False):
            transformed_code = self._split_functions(transformed_code)
        
        # 应用函数合并
        if strategy.structure.get('function_merging', False):
            transformed_code = self._merge_functions(transformed_code)
        
        # 应用调用图混淆
        if strategy.structure.get('call_graph_obfuscation', False):
            transformed_code = self._obfuscate_call_graph(transformed_code)
        
        return transformed_code
    
    def _split_functions(self, code):
        """拆分函数
        
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
            
            # 只处理较大的函数
            if len(body.strip().split('\n')) < 10:
                return match.group(0)
            
            # 拆分函数
            split_functions = self._split_function(function_name, params, body)
            
            return split_functions
        
        return function_pattern.sub(replace_function, code)
    
    def _split_function(self, function_name, params, body):
        """拆分单个函数
        
        Args:
            function_name: 函数名
            params: 函数参数
            body: 函数体
            
        Returns:
            str: 拆分后的函数代码
        """
        # 分割函数体为多个部分
        parts = self._split_body(body)
        
        if len(parts) < 2:
            return f"def {function_name}({params}):\n{body}"
        
        # 生成子函数
        sub_functions = []
        for i, part in enumerate(parts):
            sub_func_name = f"{function_name}_part_{i}_{random.randint(1000, 9999)}"
            sub_params = params  # 子函数使用相同的参数
            
            # 生成子函数定义
            sub_function = f"def {sub_func_name}({sub_params}):\n{part}"
            sub_functions.append(sub_function)
        
        # 生成主函数
        main_body = self._generate_main_function_body(function_name, sub_functions)
        main_function = f"def {function_name}({params}):\n{main_body}"
        
        # 组合所有函数
        all_functions = sub_functions + [main_function]
        
        return '\n\n'.join(all_functions)
    
    def _split_body(self, body):
        """分割函数体
        
        Args:
            body: 函数体代码
            
        Returns:
            list: 函数体部分列表
        """
        lines = body.strip().split('\n')
        if len(lines) < 10:
            return [body]
        
        # 计算每个部分的行数
        num_parts = random.randint(2, 4)
        lines_per_part = len(lines) // num_parts
        
        # 分割代码
        parts = []
        for i in range(num_parts):
            start = i * lines_per_part
            if i == num_parts - 1:
                end = len(lines)
            else:
                end = (i + 1) * lines_per_part
            
            part_lines = lines[start:end]
            part = '\n'.join(part_lines)
            parts.append(part)
        
        return parts
    
    def _generate_main_function_body(self, function_name, sub_functions):
        """生成主函数体
        
        Args:
            function_name: 函数名
            sub_functions: 子函数列表
            
        Returns:
            str: 主函数体代码
        """
        indent = ' ' * 4
        body_lines = []
        
        # 调用所有子函数
        for sub_func in sub_functions:
            # 提取子函数名
            match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', sub_func)
            if match:
                sub_func_name = match.group(1)
                body_lines.append(f"{indent}{sub_func_name}({self._extract_params(sub_func)})")
        
        # 添加返回语句（如果需要）
        if 'return' not in '\n'.join(body_lines):
            body_lines.append(f"{indent}return None")
        
        return '\n'.join(body_lines)
    
    def _extract_params(self, function_code):
        """提取函数参数
        
        Args:
            function_code: 函数代码
            
        Returns:
            str: 函数参数
        """
        match = re.search(r'def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\((.*?)\):', function_code)
        if match:
            return match.group(1)
        return ''
    
    def _merge_functions(self, code):
        """合并函数
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 寻找多个小函数
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):\s*(.*?)(?=def|$)', re.DOTALL)
        functions = function_pattern.findall(code)
        
        if len(functions) < 2:
            return code
        
        # 选择要合并的函数
        merge_candidates = []
        for func_name, params, body in functions:
            # 只合并小函数
            if len(body.strip().split('\n')) < 5:
                merge_candidates.append((func_name, params, body))
        
        if len(merge_candidates) < 2:
            return code
        
        # 随机选择2-3个函数进行合并
        num_to_merge = min(random.randint(2, 3), len(merge_candidates))
        to_merge = random.sample(merge_candidates, num_to_merge)
        
        # 生成合并后的函数
        merged_function = self._merge_function_list(to_merge)
        
        # 替换原始函数
        for func_name, _, _ in to_merge:
            pattern = re.compile(rf'def\s+{func_name}\s*\(.*?\):\s*.*?(?=def|$)', re.DOTALL)
            code = pattern.sub('', code)
        
        # 添加合并后的函数
        code = merged_function + '\n\n' + code
        
        return code
    
    def _merge_function_list(self, functions):
        """合并函数列表
        
        Args:
            functions: 函数列表 [(name, params, body), ...]
            
        Returns:
            str: 合并后的函数代码
        """
        # 生成合并后的函数名
        merged_name = f"merged_function_{random.randint(1000, 9999)}"
        
        # 合并参数
        merged_params = self._merge_params([params for _, params, _ in functions])
        
        # 合并函数体
        merged_body = self._merge_bodies([body for _, _, body in functions])
        
        # 生成合并后的函数
        return f"def {merged_name}({merged_params}):\n{merged_body}"
    
    def _merge_params(self, params_list):
        """合并参数列表
        
        Args:
            params_list: 参数列表
            
        Returns:
            str: 合并后的参数
        """
        # 收集所有参数
        all_params = set()
        for params in params_list:
            if params.strip():
                param_list = [p.strip() for p in params.split(',')]
                all_params.update(param_list)
        
        return ', '.join(all_params)
    
    def _merge_bodies(self, bodies):
        """合并函数体列表
        
        Args:
            bodies: 函数体列表
            
        Returns:
            str: 合并后的函数体
        """
        # 合并所有函数体
        merged_body = '\n\n'.join(bodies)
        
        return merged_body
    
    def _obfuscate_call_graph(self, code):
        """混淆调用图
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 生成函数映射
        func_map_name = f"_func_map_{random.randint(1000, 9999)}"
        
        # 添加函数映射到代码开头
        function_map_code = f"{func_map_name} = {{}}\n"
        
        # 提取所有函数名
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
        functions = function_pattern.findall(code)
        
        # 为每个函数添加映射
        for func_name in functions:
            function_map_code += f"{func_map_name}['{func_name}'] = {func_name}\n"
        
        # 寻找函数调用
        call_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)')
        
        def replace_call(match):
            function_name = match.group(1)
            args = match.group(2)
            
            # 跳过内置函数
            builtins = ['print', 'len', 'range', 'list', 'dict', 'tuple', 'set', 'abs', 'max', 'min']
            if function_name in builtins:
                return match.group(0)
            
            # 跳过不在函数列表中的函数
            if function_name not in functions:
                return match.group(0)
            
            # 生成间接调用
            return f"{func_map_name}['{function_name}']({args})"
        
        # 替换函数调用
        transformed_code = call_pattern.sub(replace_call, code)
        
        # 添加函数映射到代码开头
        transformed_code = function_map_code + transformed_code
        
        return transformed_code
    
    def _generate_indirect_call(self, function_name, args):
        """生成间接调用
        
        Args:
            function_name: 函数名
            args: 函数参数
            
        Returns:
            str: 间接调用代码
        """
        # 生成函数映射
        func_map_name = f"_func_map_{random.randint(1000, 9999)}"
        
        # 生成间接调用
        return f"{func_map_name}['{function_name}']({args})"
    
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
