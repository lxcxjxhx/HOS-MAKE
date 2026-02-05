"""敏感度分析器"""

class SensitivityAnalyzer:
    """敏感度分析器"""
    
    def __init__(self):
        """初始化敏感度分析器"""
        # 敏感模式列表
        self.sensitive_patterns = {
            'api_key': [r'api[_-]?key', r'api[_-]?token', r'access[_-]?token'],
            'password': [r'password', r'passwd', r'pwd'],
            'secret': [r'secret', r'private[_-]?key', r'public[_-]?key'],
            'database': [r'db[_-]?url', r'connection[_-]?string', r'db[_-]?password'],
            'hash': [r'md5', r'sha1', r'sha256', r'sha512'],
            'encryption': [r'encrypt', r'decrypt', r'cipher', r'key'],
            'token': [r'token', r'jwt', r'auth'],
            'url': [r'http[s]?://', r'ftp://'],
            'email': [r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'],
            'phone': [r'\b\d{10,15}\b'],
            'credit_card': [r'\b\d{13,16}\b'],
            'social_security': [r'\b\d{9}\b']
        }
    
    def analyze_sensitivity(self, code, ast_analyzer=None):
        """分析代码的敏感度
        
        Args:
            code: 源代码字符串
            ast_analyzer: AST分析器实例（可选）
            
        Returns:
            dict: 敏感度分析结果
        """
        # 分析敏感字符串
        sensitive_strings = self._find_sensitive_strings(code)
        
        # 分析敏感常量
        sensitive_constants = self._find_sensitive_constants(code)
        
        # 分析敏感函数
        sensitive_functions = self._find_sensitive_functions(code)
        
        # 分析敏感变量
        sensitive_variables = self._find_sensitive_variables(code)
        
        # 计算总体敏感度评分
        sensitivity_score = self._compute_sensitivity_score(
            sensitive_strings, 
            sensitive_constants, 
            sensitive_functions, 
            sensitive_variables
        )
        
        return {
            'sensitive_strings': sensitive_strings,
            'sensitive_constants': sensitive_constants,
            'sensitive_functions': sensitive_functions,
            'sensitive_variables': sensitive_variables,
            'sensitivity_score': sensitivity_score
        }
    
    def _find_sensitive_strings(self, code):
        """查找敏感字符串
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 敏感字符串列表
        """
        import re
        sensitive_strings = []
        
        # 查找字符串字面量
        string_patterns = [r'"([^"]*)"', r"'([^']*)'", r"'''([^''']*)'''"]
        
        for string_pattern in string_patterns:
            matches = re.findall(string_pattern, code, re.DOTALL)
            for match in matches:
                # 检查字符串是否包含敏感模式
                for category, patterns in self.sensitive_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, match, re.IGNORECASE):
                            sensitive_strings.append({
                                'content': match,
                                'category': category,
                                'pattern': pattern
                            })
                            break
        
        return sensitive_strings
    
    def _find_sensitive_constants(self, code):
        """查找敏感常量
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 敏感常量列表
        """
        import re
        sensitive_constants = []
        
        # 查找常量定义（全大写变量）
        constant_pattern = r'\b([A-Z_][A-Z0-9_]*)\s*=\s*(.*)'
        matches = re.findall(constant_pattern, code)
        
        for name, value in matches:
            # 检查常量名是否包含敏感模式
            for category, patterns in self.sensitive_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, name, re.IGNORECASE):
                        sensitive_constants.append({
                            'name': name,
                            'value': value,
                            'category': category,
                            'pattern': pattern
                        })
                        break
            
            # 检查常量值是否包含敏感模式
            if value:
                for category, patterns in self.sensitive_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, value, re.IGNORECASE):
                            sensitive_constants.append({
                                'name': name,
                                'value': value,
                                'category': category,
                                'pattern': pattern
                            })
                            break
        
        return sensitive_constants
    
    def _find_sensitive_functions(self, code):
        """查找敏感函数
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 敏感函数列表
        """
        import re
        sensitive_functions = []
        
        # 查找函数定义
        function_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        matches = re.findall(function_pattern, code)
        
        for function_name in matches:
            # 检查函数名是否包含敏感模式
            for category, patterns in self.sensitive_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, function_name, re.IGNORECASE):
                        sensitive_functions.append({
                            'name': function_name,
                            'category': category,
                            'pattern': pattern
                        })
                        break
        
        # 查找函数调用
        function_call_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        call_matches = re.findall(function_call_pattern, code)
        
        for function_name in call_matches:
            # 跳过已经识别的函数定义
            if function_name not in [f['name'] for f in sensitive_functions]:
                # 检查函数名是否包含敏感模式
                for category, patterns in self.sensitive_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, function_name, re.IGNORECASE):
                            sensitive_functions.append({
                                'name': function_name,
                                'category': category,
                                'pattern': pattern,
                                'is_call': True
                            })
                            break
        
        return sensitive_functions
    
    def _find_sensitive_variables(self, code):
        """查找敏感变量
        
        Args:
            code: 源代码字符串
            
        Returns:
            list: 敏感变量列表
        """
        import re
        sensitive_variables = []
        
        # 查找变量赋值
        variable_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*='
        matches = re.findall(variable_pattern, code)
        
        # 过滤掉函数定义中的参数
        function_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)'
        function_matches = re.findall(function_pattern, code)
        function_params = set()
        for _, params in function_matches:
            param_list = params.split(',')
            for param in param_list:
                param = param.strip()
                if param:
                    param_name = param.split('=')[0].strip()
                    function_params.add(param_name)
        
        for variable_name in matches:
            # 跳过函数参数
            if variable_name in function_params:
                continue
            
            # 检查变量名是否包含敏感模式
            for category, patterns in self.sensitive_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, variable_name, re.IGNORECASE):
                        sensitive_variables.append({
                            'name': variable_name,
                            'category': category,
                            'pattern': pattern
                        })
                        break
        
        return sensitive_variables
    
    def _compute_sensitivity_score(self, sensitive_strings, sensitive_constants, sensitive_functions, sensitive_variables):
        """计算敏感度评分
        
        Args:
            sensitive_strings: 敏感字符串列表
            sensitive_constants: 敏感常量列表
            sensitive_functions: 敏感函数列表
            sensitive_variables: 敏感变量列表
            
        Returns:
            float: 敏感度评分（0-100）
        """
        # 基础分数
        base_score = 0
        
        # 每个敏感项的权重
        weights = {
            'strings': 3,
            'constants': 3,
            'functions': 2,
            'variables': 2
        }
        
        # 计算总分数
        total_score = (
            len(sensitive_strings) * weights['strings'] +
            len(sensitive_constants) * weights['constants'] +
            len(sensitive_functions) * weights['functions'] +
            len(sensitive_variables) * weights['variables']
        )
        
        # 归一化到0-100
        max_possible_score = 50  # 假设最多有10个敏感项
        sensitivity_score = min(100, (total_score / max_possible_score) * 100)
        
        return sensitivity_score
    
    def get_sensitive_categories(self):
        """获取敏感类别列表
        
        Returns:
            list: 敏感类别列表
        """
        return list(self.sensitive_patterns.keys())
    
    def add_sensitive_pattern(self, category, pattern):
        """添加敏感模式
        
        Args:
            category: 敏感类别
            pattern: 正则表达式模式
        """
        if category not in self.sensitive_patterns:
            self.sensitive_patterns[category] = []
        self.sensitive_patterns[category].append(pattern)
    
    def remove_sensitive_pattern(self, category, pattern):
        """移除敏感模式
        
        Args:
            category: 敏感类别
            pattern: 正则表达式模式
        """
        if category in self.sensitive_patterns:
            if pattern in self.sensitive_patterns[category]:
                self.sensitive_patterns[category].remove(pattern)
