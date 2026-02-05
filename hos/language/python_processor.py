"""Python语言处理器"""

from hos.language.base import LanguageProcessor
from hos.analyzer import analyze
from hos.transformer import transform

class PythonProcessor(LanguageProcessor):
    """Python语言处理器
    
    实现对Python代码的分析和转换。
    """
    
    def __init__(self):
        """初始化Python语言处理器"""
        super().__init__()
    
    def analyze(self, code):
        """分析Python代码
        
        Args:
            code: Python源代码字符串
            
        Returns:
            dict: 分析结果
        """
        return analyze(code)
    
    def transform(self, code, strategy):
        """转换Python代码
        
        Args:
            code: Python源代码字符串
            strategy: 混淆策略
            
        Returns:
            str: 转换后的代码
        """
        return transform(code, strategy)
    
    def get_file_extensions(self):
        """获取支持的文件扩展名
        
        Returns:
            list: 文件扩展名列表
        """
        return ['.py']
    
    def get_language_name(self):
        """获取语言名称
        
        Returns:
            str: 语言名称
        """
        return 'python'
