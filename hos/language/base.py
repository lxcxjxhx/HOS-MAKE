"""语言处理器基类"""

class LanguageProcessor:
    """语言处理器基类
    
    所有语言特定的处理器都应该继承这个类并实现其方法。
    """
    
    def __init__(self):
        """初始化语言处理器"""
        pass
    
    def analyze(self, code):
        """分析代码
        
        Args:
            code: 源代码字符串
            
        Returns:
            dict: 分析结果
        """
        raise NotImplementedError("子类必须实现analyze方法")
    
    def transform(self, code, strategy):
        """转换代码
        
        Args:
            code: 源代码字符串
            strategy: 混淆策略
            
        Returns:
            str: 转换后的代码
        """
        raise NotImplementedError("子类必须实现transform方法")
    
    def get_file_extensions(self):
        """获取支持的文件扩展名
        
        Returns:
            list: 文件扩展名列表
        """
        raise NotImplementedError("子类必须实现get_file_extensions方法")
    
    def get_language_name(self):
        """获取语言名称
        
        Returns:
            str: 语言名称
        """
        raise NotImplementedError("子类必须实现get_language_name方法")
