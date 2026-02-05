"""语言处理器工厂"""

from hos.language.detector import LanguageDetector
from hos.language.python_processor import PythonProcessor
from hos.language.cpp_processor import CPPProcessor
from hos.language.rust_processor import RustProcessor
from hos.language.go_processor import GoProcessor
from hos.language.arm_processor import ARMProcessor
from hos.language.wasm_processor import WASMProcessor

class ProcessorFactory:
    """语言处理器工厂
    
    根据语言类型创建相应的语言处理器。
    """
    
    def __init__(self):
        """初始化处理器工厂"""
        self.detector = LanguageDetector()
        self.processors = {
            'python': PythonProcessor,
            'c': CPPProcessor,
            'cpp': CPPProcessor,
            'rust': RustProcessor,
            'go': GoProcessor,
            'arm': ARMProcessor,
            'wasm': WASMProcessor
        }
    
    def get_processor(self, language):
        """根据语言获取处理器
        
        Args:
            language: 语言名称
            
        Returns:
            LanguageProcessor: 语言处理器实例
        """
        if language in self.processors:
            return self.processors[language]()
        else:
            raise ValueError(f"不支持的语言: {language}")
    
    def get_processor_from_file(self, file_path):
        """从文件获取处理器
        
        Args:
            file_path: 文件路径
            
        Returns:
            LanguageProcessor: 语言处理器实例
        """
        language = self.detector.detect_from_file(file_path)
        return self.get_processor(language)
    
    def get_processor_from_content(self, code):
        """从代码内容获取处理器
        
        Args:
            code: 代码内容
            
        Returns:
            LanguageProcessor: 语言处理器实例
        """
        language = self.detector.detect_from_content(code)
        return self.get_processor(language)
    
    def register_processor(self, language, processor_class):
        """注册新的语言处理器
        
        Args:
            language: 语言名称
            processor_class: 处理器类
        """
        self.processors[language] = processor_class
    
    def get_supported_languages(self):
        """获取支持的语言列表
        
        Returns:
            list: 支持的语言列表
        """
        return list(self.processors.keys())
