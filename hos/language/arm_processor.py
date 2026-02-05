"""ARM语言处理器"""

from hos.language.base import LanguageProcessor
import re

class ARMProcessor(LanguageProcessor):
    """ARM语言处理器
    
    实现对ARM汇编代码的分析和转换，支持Android NDK/ARM平台。
    """
    
    def __init__(self):
        """初始化ARM语言处理器"""
        super().__init__()
    
    def analyze(self, code):
        """分析ARM汇编代码
        
        Args:
            code: ARM汇编源代码字符串
            
        Returns:
            dict: 分析结果
        """
        # 提取基本信息
        functions = self._extract_functions(code)
        instructions = self._extract_instructions(code)
        registers = self._extract_registers(code)
        
        # 生成分析结果
        analysis_result = {
            'ast': {
                'functions': functions,
                'classes': [],
                'imports': []
            },
            'cfg': {
                'entry': {'id': 1, 'type': 'entry'},
                'exit': {'id': 2, 'type': 'exit'},
                'nodes': {
                    1: {'id': 1, 'type': 'entry', 'successors': [2]},
                    2: {'id': 2, 'type': 'exit', 'successors': []}
                }
            },
            'data_flow': {
                'reaching_definitions': {},
                'live_variables': {
                    'in_sets': {},
                    'out_sets': {}
                }
            },
            'hot_paths': [],
            'sensitivity': {
                'sensitivity_score': 50,
                'sensitive_strings': [],
                'sensitive_constants': self._extract_constants(code),
                'sensitive_functions': [],
                'sensitive_variables': registers
            },
            'code_size': len(code),
            'line_count': len(code.split('\n'))
        }
        
        # 计算安全价值评分
        analysis_result['security_score'] = self._compute_security_score(analysis_result)
        
        return analysis_result
    
    def transform(self, code, strategy):
        """转换ARM汇编代码
        
        Args:
            code: ARM汇编源代码字符串
            strategy: 混淆策略
            
        Returns:
            str: 转换后的代码
        """
        transformed_code = code
        
        # 应用控制流混淆
        if strategy.control_flow.get('flattening', False):
            transformed_code = self._obfuscate_control_flow(transformed_code)
        
        # 应用数据混淆
        if strategy.data.get('constant_splitting', False):
            transformed_code = self._split_constants(transformed_code)
        
        # 应用寄存器混淆
        if strategy.control_flow.get('register_allocation', False):
            transformed_code = self._obfuscate_registers(transformed_code)
        
        return transformed_code
    
    def get_file_extensions(self):
        """获取支持的文件扩展名
        
        Returns:
            list: 文件扩展名列表
        """
        return ['.s', '.S', '.asm']
    
    def get_language_name(self):
        """获取语言名称
        
        Returns:
            str: 语言名称
        """
        return 'arm'
    
    def _extract_functions(self, code):
        """提取函数定义
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 函数列表
        """
        functions = []
        # 简单的函数提取正则表达式
        function_pattern = re.compile(r'\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*', re.MULTILINE)
        
        for match in function_pattern.finditer(code):
            name = match.group(1)
            functions.append({
                'name': name,
                'params': '',
                'return_type': '',
                'body': ''
            })
        
        return functions
    
    def _extract_instructions(self, code):
        """提取指令
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 指令列表
        """
        instructions = []
        # 简单的指令提取正则表达式
        instruction_pattern = re.compile(r'\s*([a-z]+)\s+.*', re.MULTILINE)
        
        for match in instruction_pattern.finditer(code):
            instructions.append(match.group(1))
        
        return instructions
    
    def _extract_registers(self, code):
        """提取寄存器
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 寄存器列表
        """
        registers = []
        # 简单的寄存器提取正则表达式
        register_pattern = re.compile(r'\s*[a-z]+\s+.*?([rR][0-9]+|sp|lr|pc).*', re.MULTILINE)
        
        for match in register_pattern.finditer(code):
            registers.append(match.group(1))
        
        return list(set(registers))
    
    def _extract_constants(self, code):
        """提取常量
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 常量列表
        """
        constants = []
        # 简单的常量提取正则表达式
        const_pattern = re.compile(r'\s*[a-z]+\s+.*?#([0-9]+).*', re.MULTILINE)
        
        for match in const_pattern.finditer(code):
            constants.append(match.group(1))
        
        return constants
    
    def _compute_security_score(self, analysis_result):
        """计算安全价值评分
        
        Args:
            analysis_result: 分析结果
            
        Returns:
            float: 安全价值评分
        """
        score = 0.0
        
        # 基于代码复杂度
        line_count = analysis_result['line_count']
        if line_count > 1000:
            score += 20
        elif line_count > 500:
            score += 15
        elif line_count > 100:
            score += 10
        else:
            score += 5
        
        # 基于函数数量
        function_count = len(analysis_result['ast']['functions'])
        if function_count > 50:
            score += 15
        elif function_count > 20:
            score += 10
        elif function_count > 5:
            score += 5
        else:
            score += 2
        
        # 基于敏感度评分
        sensitivity_score = analysis_result['sensitivity']['sensitivity_score']
        score += sensitivity_score * 0.3
        
        # 归一化到0-100
        score = min(100, score)
        
        return score
    
    def _obfuscate_control_flow(self, code):
        """混淆控制流
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 混淆后的代码
        """
        # 简单的控制流混淆实现
        # 这里只是一个示例，实际实现需要更复杂的分析
        return code
    
    def _split_constants(self, code):
        """拆分常量
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 拆分后的代码
        """
        # 简单的常量拆分实现
        # 这里只是一个示例，实际实现需要更复杂的分析
        return code
    
    def _obfuscate_registers(self, code):
        """混淆寄存器
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 混淆后的代码
        """
        # 简单的寄存器混淆实现
        # 这里只是一个示例，实际实现需要更复杂的分析
        return code
