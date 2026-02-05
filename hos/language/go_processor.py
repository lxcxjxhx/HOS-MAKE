"""Go语言处理器"""

from hos.language.base import LanguageProcessor
import re

class GoProcessor(LanguageProcessor):
    """Go语言处理器
    
    实现对Go代码的分析和转换。
    """
    
    def __init__(self):
        """初始化Go语言处理器"""
        super().__init__()
    
    def analyze(self, code):
        """分析Go代码
        
        Args:
            code: Go源代码字符串
            
        Returns:
            dict: 分析结果
        """
        # 提取基本信息
        functions = self._extract_functions(code)
        structs = self._extract_structs(code)
        interfaces = self._extract_interfaces(code)
        imports = self._extract_imports(code)
        
        # 生成分析结果
        analysis_result = {
            'ast': {
                'functions': functions,
                'classes': structs + interfaces,  # 将struct和interface视为类
                'imports': imports
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
                'sensitive_strings': self._extract_strings(code),
                'sensitive_constants': self._extract_constants(code),
                'sensitive_functions': [],
                'sensitive_variables': []
            },
            'code_size': len(code),
            'line_count': len(code.split('\n'))
        }
        
        # 计算安全价值评分
        analysis_result['security_score'] = self._compute_security_score(analysis_result)
        
        return analysis_result
    
    def transform(self, code, strategy):
        """转换Go代码
        
        Args:
            code: Go源代码字符串
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
        
        if strategy.data.get('string_encryption', False):
            transformed_code = self._encrypt_strings(transformed_code)
        
        return transformed_code
    
    def get_file_extensions(self):
        """获取支持的文件扩展名
        
        Returns:
            list: 文件扩展名列表
        """
        return ['.go']
    
    def get_language_name(self):
        """获取语言名称
        
        Returns:
            str: 语言名称
        """
        return 'go'
    
    def _extract_functions(self, code):
        """提取函数定义
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 函数列表
        """
        functions = []
        # 简单的函数提取正则表达式
        function_pattern = re.compile(r'\s*func\s+(?:\(.*?\)\s+)?(\w+)\s*\(([^)]*)\)\s*(?:\s+([^\{]+))?\s*[{]', re.MULTILINE)
        
        for match in function_pattern.finditer(code):
            name = match.group(1)
            params = match.group(2)
            return_type = match.group(3) if match.group(3) else ''
            
            functions.append({
                'name': name,
                'params': params,
                'return_type': return_type.strip(),
                'body': ''
            })
        
        return functions
    
    def _extract_structs(self, code):
        """提取结构体定义
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 结构体列表
        """
        structs = []
        # 简单的结构体提取正则表达式
        struct_pattern = re.compile(r'\s*type\s+(\w+)\s+struct\s*[{]', re.MULTILINE)
        
        for match in struct_pattern.finditer(code):
            name = match.group(1)
            structs.append({
                'name': name,
                'type': 'struct',
                'methods': []
            })
        
        return structs
    
    def _extract_interfaces(self, code):
        """提取接口定义
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 接口列表
        """
        interfaces = []
        # 简单的接口提取正则表达式
        interface_pattern = re.compile(r'\s*type\s+(\w+)\s+interface\s*[{]', re.MULTILINE)
        
        for match in interface_pattern.finditer(code):
            name = match.group(1)
            interfaces.append({
                'name': name,
                'type': 'interface',
                'methods': []
            })
        
        return interfaces
    
    def _extract_imports(self, code):
        """提取导入语句
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 导入语句列表
        """
        imports = []
        # 简单的导入提取正则表达式
        import_pattern = re.compile(r'\s*import\s+[\(]?\s*([^\)]+)\s*[\)]?', re.MULTILINE | re.DOTALL)
        
        for match in import_pattern.finditer(code):
            import_content = match.group(1)
            # 提取每个导入的包
            pkg_pattern = re.compile(r'["]([^"\n]+)["]', re.MULTILINE)
            for pkg_match in pkg_pattern.finditer(import_content):
                imports.append(pkg_match.group(1))
        
        return imports
    
    def _extract_strings(self, code):
        """提取字符串常量
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 字符串列表
        """
        strings = []
        # 简单的字符串提取正则表达式
        string_pattern = re.compile(r'"([^"]*)"', re.MULTILINE)
        
        for match in string_pattern.finditer(code):
            strings.append(match.group(1))
        
        return strings
    
    def _extract_constants(self, code):
        """提取常量
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 常量列表
        """
        constants = []
        # 简单的常量提取正则表达式
        const_pattern = re.compile(r'\s*const\s+(?:\(\s*([^\)]+)\s*\)|(\w+)\s*=\s*([^;]+))', re.MULTILINE | re.DOTALL)
        
        for match in const_pattern.finditer(code):
            if match.group(1):
                # 处理常量块
                const_block = match.group(1)
                const_line_pattern = re.compile(r'\s*\w+\s*=\s*([^\n]+)', re.MULTILINE)
                for const_line_match in const_line_pattern.finditer(const_block):
                    constants.append(const_line_match.group(1))
            elif match.group(3):
                # 处理单行常量
                constants.append(match.group(3))
        
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
        
        # 基于类数量
        class_count = len(analysis_result['ast']['classes'])
        if class_count > 20:
            score += 10
        elif class_count > 10:
            score += 7
        elif class_count > 3:
            score += 4
        else:
            score += 1
        
        # 基于敏感度评分
        sensitivity_score = analysis_result['sensitivity']['sensitivity_score']
        score += sensitivity_score * 0.3
        
        # 基于导入模块数量
        import_count = len(analysis_result['ast']['imports'])
        if import_count > 20:
            score += 8
        elif import_count > 10:
            score += 5
        elif import_count > 3:
            score += 2
        else:
            score += 1
        
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
    
    def _encrypt_strings(self, code):
        """加密字符串
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 加密后的代码
        """
        # 简单的字符串加密实现
        # 这里只是一个示例，实际实现需要更复杂的分析
        return code
