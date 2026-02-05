"""代码变换引擎主入口"""

from hos.transformer.control_flow import ControlFlowTransformer
from hos.transformer.data import DataTransformer
from hos.transformer.instruction import InstructionTransformer
from hos.transformer.structure import StructureTransformer
from hos.transformer.virtualization import VirtualizationTransformer
from hos.transformer.runtime import RuntimeProtector

class CodeTransformer:
    """代码变换器"""
    
    def __init__(self):
        """初始化代码变换器"""
        self.control_flow_transformer = ControlFlowTransformer()
        self.data_transformer = DataTransformer()
        self.instruction_transformer = InstructionTransformer()
        self.structure_transformer = StructureTransformer()
        self.virtualization_transformer = VirtualizationTransformer()
        self.runtime_protector = RuntimeProtector()
    
    def transform(self, code, strategy):
        """变换代码
        
        Args:
            code: 源代码字符串
            strategy: 混淆策略
            
        Returns:
            str: 变换后的代码
        """
        transformed_code = code
        
        # 应用控制流变换
        transformed_code = self.control_flow_transformer.transform(transformed_code, strategy)
        
        # 应用数据变换
        transformed_code = self.data_transformer.transform(transformed_code, strategy)
        
        # 应用指令级变换
        transformed_code = self.instruction_transformer.transform(transformed_code, strategy)
        
        # 应用结构级变换
        transformed_code = self.structure_transformer.transform(transformed_code, strategy)
        
        # 应用虚拟化变换
        transformed_code = self.virtualization_transformer.transform(transformed_code, strategy)
        
        # 应用运行时保护
        transformed_code = self.runtime_protector.transform(transformed_code, strategy)
        
        return transformed_code
    
    def transform_file(self, input_path, output_path, strategy):
        """变换文件
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            strategy: 混淆策略
        """
        # 读取文件
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 变换代码
        transformed_code = self.transform(code, strategy)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transformed_code)

# 便捷函数
def transform(code, strategy):
    """变换代码的便捷函数
    
    Args:
        code: 源代码字符串
        strategy: 混淆策略
        
    Returns:
        str: 变换后的代码
    """
    transformer = CodeTransformer()
    return transformer.transform(code, strategy)

def transform_file(input_path, output_path, strategy):
    """变换文件的便捷函数
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        strategy: 混淆策略
    """
    transformer = CodeTransformer()
    transformer.transform_file(input_path, output_path, strategy)
