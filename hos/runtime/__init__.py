"""运行时保护层模块"""

from hos.transformer.runtime import RuntimeProtector
from hos.ai.strategy import ConfusionStrategy

def protect(code, security_level='medium'):
    """保护代码
    
    Args:
        code: 源代码字符串
        security_level: 安全级别（'low', 'medium', 'high'）
        
    Returns:
        str: 保护后的代码
    """
    # 创建混淆策略
    strategy = ConfusionStrategy()
    
    # 设置安全级别
    if security_level == 'low':
        strategy.set_strength(0.3)
        strategy.runtime['debugger_detection'] = False
        strategy.runtime['memory_integrity'] = False
        strategy.runtime['timing_detection'] = False
        strategy.runtime['environment_binding'] = False
        strategy.runtime['anti_tampering'] = False
    elif security_level == 'medium':
        strategy.set_strength(0.5)
        strategy.runtime['debugger_detection'] = True
        strategy.runtime['memory_integrity'] = True
        strategy.runtime['timing_detection'] = True
        strategy.runtime['environment_binding'] = False
        strategy.runtime['anti_tampering'] = True
    else:  # high
        strategy.set_strength(0.8)
        strategy.runtime['debugger_detection'] = True
        strategy.runtime['memory_integrity'] = True
        strategy.runtime['timing_detection'] = True
        strategy.runtime['environment_binding'] = True
        strategy.runtime['anti_tampering'] = True
    
    # 创建运行时保护层
    protector = RuntimeProtector()
    
    # 应用保护
    protected_code = protector.transform(code, strategy)
    
    return protected_code

__all__ = ["protect"]