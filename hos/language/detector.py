"""语言检测器"""

import os
import re

class LanguageDetector:
    """语言检测器
    
    用于检测代码的编程语言，基于文件扩展名和内容分析。
    """
    
    def __init__(self):
        """初始化语言检测器"""
        # 文件扩展名映射到语言
        self.extension_map = {
            '.py': 'python',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.h': 'c',
            '.hpp': 'cpp',
            '.rs': 'rust',
            '.go': 'go',
            '.java': 'java',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.wasm': 'wasm'
        }
        
        # 内容特征映射
        self.content_patterns = {
            'python': [r'^\s*def\s+\w+\s*\(', r'^\s*import\s+\w+', r'^\s*from\s+\w+\s+import'],
            'c': [r'^\s*#include\s*<\w+\.h>', r'^\s*int\s+main\s*\(', r'^\s*void\s+\w+\s*\('],
            'cpp': [r'^\s*#include\s*<\w+\.hpp>', r'^\s*class\s+\w+', r'^\s*namespace\s+\w+'],
            'rust': [r'^\s*fn\s+\w+\s*\(', r'^\s*use\s+\w+', r'^\s*mod\s+\w+'],
            'go': [r'^\s*package\s+\w+', r'^\s*import\s+\(', r'^\s*func\s+\w+\s*\('],
            'java': [r'^\s*public\s+class\s+\w+', r'^\s*import\s+\w+', r'^\s*package\s+\w+'],
            'javascript': [r'^\s*function\s+\w+\s*\(', r'^\s*const\s+\w+\s*=', r'^\s*let\s+\w+\s*='],
            'typescript': [r'^\s*interface\s+\w+', r'^\s*type\s+\w+\s*=', r'^\s*import\s+.*from'],
            'wasm': [r'^\s*\(module', r'^\s*\(func', r'^\s*\(export']
        }
    
    def detect_from_file(self, file_path):
        """从文件中检测语言
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 检测到的语言
        """
        # 首先根据文件扩展名检测
        extension = os.path.splitext(file_path)[1].lower()
        if extension in self.extension_map:
            return self.extension_map[extension]
        
        # 如果扩展名无法确定，尝试从内容检测
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.detect_from_content(content)
        except Exception:
            return 'unknown'
    
    def detect_from_content(self, code):
        """从代码内容中检测语言
        
        Args:
            code: 代码内容
            
        Returns:
            str: 检测到的语言
        """
        # 统计每种语言的匹配次数
        scores = {}
        for language, patterns in self.content_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, code, re.MULTILINE):
                    score += 1
            scores[language] = score
        
        # 返回得分最高的语言
        if scores:
            return max(scores, key=scores.get)
        return 'unknown'
    
    def detect_from_extension(self, extension):
        """根据文件扩展名检测语言
        
        Args:
            extension: 文件扩展名（带或不带点）
            
        Returns:
            str: 检测到的语言
        """
        if not extension.startswith('.'):
            extension = '.' + extension
        return self.extension_map.get(extension.lower(), 'unknown')
    
    def is_supported(self, language):
        """检查语言是否被支持
        
        Args:
            language: 语言名称
            
        Returns:
            bool: 是否被支持
        """
        return language in self.content_patterns
