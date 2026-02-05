"""AST分析器"""

class ASTAnalyzer:
    """基于简化实现的AST分析器"""
    
    def __init__(self):
        """初始化AST分析器"""
        # 简化实现，不依赖tree-sitter
        pass
    
    def parse(self, code):
        """解析代码生成AST
        
        Args:
            code: 源代码字符串
            
        Returns:
            dict: 简化的AST结构
        """
        return {
            'code': code
        }
    
    def get_root_node(self, tree):
        """获取AST根节点
        
        Args:
            tree: 抽象语法树
            
        Returns:
            dict: 简化的根节点
        """
        return {
            'type': 'program',
            'code': tree['code']
        }
    
    def traverse(self, node, callback):
        """遍历AST节点
        
        Args:
            node: 起始节点
            callback: 回调函数，接收节点作为参数
        """
        callback(node)
    
    def find_nodes_by_type(self, node, node_type):
        """查找指定类型的节点
        
        Args:
            node: 起始节点
            node_type: 节点类型
            
        Returns:
            list: 匹配的节点列表
        """
        import re
        nodes = []
        
        if node_type == 'function_definition':
            # 简单的正则表达式匹配函数定义
            function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):')
            for match in function_pattern.finditer(node['code']):
                nodes.append({
                    'type': 'function_definition',
                    'name': match.group(1),
                    'parameters': match.group(2),
                    'start_point': (0, 0),
                    'end_point': (0, 0)
                })
        elif node_type == 'class_definition':
            # 简单的正则表达式匹配类定义
            class_pattern = re.compile(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):')
            for match in class_pattern.finditer(node['code']):
                nodes.append({
                    'type': 'class_definition',
                    'name': match.group(1),
                    'start_point': (0, 0),
                    'end_point': (0, 0)
                })
        elif node_type == 'import_statement':
            # 简单的正则表达式匹配导入语句
            import_pattern = re.compile(r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*)')
            for match in import_pattern.finditer(node['code']):
                nodes.append({
                    'type': 'import_statement',
                    'module': match.group(1)
                })
        elif node_type == 'from_import_statement':
            # 简单的正则表达式匹配from导入语句
            from_import_pattern = re.compile(r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import')
            for match in from_import_pattern.finditer(node['code']):
                nodes.append({
                    'type': 'from_import_statement',
                    'module': match.group(1)
                })
        
        return nodes
    
    def get_node_text(self, node, code):
        """获取节点对应的源代码文本
        
        Args:
            node: 节点
            code: 源代码字符串
            
        Returns:
            str: 节点对应的文本
        """
        if 'name' in node:
            return node['name']
        elif 'module' in node:
            return node['module']
        return ''
    
    def analyze_function(self, function_node, code):
        """分析函数节点
        
        Args:
            function_node: 函数定义节点
            code: 源代码字符串
            
        Returns:
            dict: 函数分析结果
        """
        return {
            'name': function_node['name'],
            'parameters': function_node['parameters'].split(',') if function_node['parameters'] else [],
            'body': function_node,
            'start_line': 1,
            'end_line': 1
        }
    
    def analyze_imports(self, root_node, code):
        """分析导入语句
        
        Args:
            root_node: 根节点
            code: 源代码字符串
            
        Returns:
            list: 导入模块列表
        """
        imports = []
        
        # 分析import语句
        for node in self.find_nodes_by_type(root_node, 'import_statement'):
            imports.append(node['module'])
        
        # 分析from import语句
        for node in self.find_nodes_by_type(root_node, 'from_import_statement'):
            imports.append(node['module'])
        
        return imports
    
    def get_code_structure(self, code):
        """获取代码结构
        
        Args:
            code: 源代码字符串
            
        Returns:
            dict: 代码结构分析结果
        """
        # 解析代码
        tree = self.parse(code)
        root_node = self.get_root_node(tree)
        
        # 分析函数
        functions = []
        for function_node in self.find_nodes_by_type(root_node, 'function_definition'):
            functions.append(self.analyze_function(function_node, code))
        
        # 分析类
        classes = []
        for class_node in self.find_nodes_by_type(root_node, 'class_definition'):
            classes.append({
                'name': class_node['name'],
                'methods': [],
                'start_line': 1,
                'end_line': 1
            })
        
        # 分析导入
        imports = self.analyze_imports(root_node, code)
        
        return {
            'functions': functions,
            'classes': classes,
            'imports': imports,
            'tree': tree,
            'root_node': root_node
        }
