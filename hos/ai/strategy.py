"""混淆策略类"""

class ConfusionStrategy:
    """混淆策略"""
    
    def __init__(self):
        """初始化混淆策略"""
        # 控制流混淆策略
        self.control_flow = {
            'flattening': False,  # 控制流平坦化
            'fake_branches': False,  # 伪分支
            'exception_flow': False,  # 异常驱动流
            'loop_transform': False,  # 循环变换
            'strength': 0.5  # 混淆强度（0-1）
        }
        
        # 数据混淆策略
        self.data = {
            'constant_splitting': False,  # 常量拆分
            'dynamic_calculation': False,  # 动态计算
            'encoding_table': False,  # 编码表
            'string_encryption': False,  # 字符串加密
            'strength': 0.5  # 混淆强度（0-1）
        }
        
        # 指令级混淆策略
        self.instruction = {
            'garbage_injection': False,  # 垃圾指令注入
            'instruction_substitution': False,  # 等价指令替换
            'register_allocation': False,  # 寄存器分配混淆
            'strength': 0.5  # 混淆强度（0-1）
        }
        
        # 结构级混淆策略
        self.structure = {
            'function_splitting': False,  # 函数拆分
            'function_merging': False,  # 函数合并
            'call_graph_obfuscation': False,  # 调用图混淆
            'strength': 0.5  # 混淆强度（0-1）
        }
        
        # 虚拟化策略
        self.virtualization = {
            'enabled': False,  # 是否启用
            'bytecode_vm': False,  # 字节码VM
            'interpreted_execution': False,  # 解释执行
            'strength': 0.5  # 混淆强度（0-1）
        }
        
        # 运行时保护策略
        self.runtime = {
            'debugger_detection': False,  # 调试器检测
            'memory_integrity': False,  # 内存完整性校验
            'timing_detection': False,  # 时序检测
            'environment_binding': False,  # 环境绑定
            'anti_tampering': False,  # 防篡改
            'strength': 0.5  # 保护强度（0-1）
        }
        
        # 性能控制
        self.performance = {
            'max_instruction_expansion': 2.0,  # 最大指令膨胀率
            'max_function_overhead': 1.5,  # 最大函数调用开销
            'hot_path_protection': False,  # 热路径保护
            'auto_balance': True  # 自动平衡性能与安全
        }
        
        # 目标平台
        self.platform = {
            'os': 'all',  # 操作系统
            'architecture': 'all',  # 架构
            'language': 'python',  # 语言
            'version': '3.8+'  # 版本
        }
    
    def from_dict(self, data):
        """从字典加载策略
        
        Args:
            data: 策略字典
        """
        if 'control_flow' in data:
            self.control_flow.update(data['control_flow'])
        if 'data' in data:
            self.data.update(data['data'])
        if 'instruction' in data:
            self.instruction.update(data['instruction'])
        if 'structure' in data:
            self.structure.update(data['structure'])
        if 'virtualization' in data:
            self.virtualization.update(data['virtualization'])
        if 'runtime' in data:
            self.runtime.update(data['runtime'])
        if 'performance' in data:
            self.performance.update(data['performance'])
        if 'platform' in data:
            self.platform.update(data['platform'])
    
    def to_dict(self):
        """转换为字典
        
        Returns:
            dict: 策略字典
        """
        return {
            'control_flow': self.control_flow,
            'data': self.data,
            'instruction': self.instruction,
            'structure': self.structure,
            'virtualization': self.virtualization,
            'runtime': self.runtime,
            'performance': self.performance,
            'platform': self.platform
        }
    
    def set_strength(self, strength):
        """设置整体混淆强度
        
        Args:
            strength: 混淆强度（0-1）
        """
        strength = max(0, min(1, strength))
        
        self.control_flow['strength'] = strength
        self.data['strength'] = strength
        self.instruction['strength'] = strength
        self.structure['strength'] = strength
        self.virtualization['strength'] = strength
        self.runtime['strength'] = strength
        
        # 根据强度自动启用相应的混淆技术
        if strength >= 0.3:
            self.control_flow['fake_branches'] = True
            self.data['constant_splitting'] = True
            self.instruction['garbage_injection'] = True
        
        if strength >= 0.5:
            self.control_flow['flattening'] = True
            self.data['dynamic_calculation'] = True
            self.data['string_encryption'] = True
            self.instruction['instruction_substitution'] = True
            self.structure['function_splitting'] = True
            self.runtime['debugger_detection'] = True
        
        if strength >= 0.7:
            self.control_flow['exception_flow'] = True
            self.control_flow['loop_transform'] = True
            self.data['encoding_table'] = True
            self.instruction['register_allocation'] = True
            self.structure['function_merging'] = True
            self.structure['call_graph_obfuscation'] = True
            self.runtime['memory_integrity'] = True
            self.runtime['timing_detection'] = True
        
        if strength >= 0.9:
            self.virtualization['enabled'] = True
            self.virtualization['bytecode_vm'] = True
            self.virtualization['interpreted_execution'] = True
            self.runtime['environment_binding'] = True
            self.runtime['anti_tampering'] = True
    
    def set_performance_mode(self, mode):
        """设置性能模式
        
        Args:
            mode: 性能模式（'balanced', 'performance', 'security'）
        """
        if mode == 'performance':
            self.performance['max_instruction_expansion'] = 1.2
            self.performance['max_function_overhead'] = 1.1
            self.performance['hot_path_protection'] = True
            self.set_strength(0.3)
        elif mode == 'security':
            self.performance['max_instruction_expansion'] = 3.0
            self.performance['max_function_overhead'] = 2.0
            self.performance['hot_path_protection'] = False
            self.set_strength(0.8)
        else:  # balanced
            self.performance['max_instruction_expansion'] = 2.0
            self.performance['max_function_overhead'] = 1.5
            self.performance['hot_path_protection'] = True
            self.set_strength(0.5)
    
    def validate(self):
        """验证策略有效性
        
        Returns:
            bool: 策略是否有效
        """
        # 检查强度值是否在有效范围内
        for section in [self.control_flow, self.data, self.instruction, self.structure, self.virtualization, self.runtime]:
            if 'strength' in section:
                strength = section['strength']
                if not (0 <= strength <= 1):
                    return False
        
        # 检查性能控制值
        if self.performance['max_instruction_expansion'] < 1.0:
            return False
        if self.performance['max_function_overhead'] < 1.0:
            return False
        
        return True
    
    def get_security_score(self):
        """计算安全评分
        
        Returns:
            float: 安全评分（0-100）
        """
        score = 0.0
        
        # 控制流混淆评分
        if self.control_flow['flattening']:
            score += 15
        if self.control_flow['fake_branches']:
            score += 5
        if self.control_flow['exception_flow']:
            score += 10
        if self.control_flow['loop_transform']:
            score += 8
        
        # 数据混淆评分
        if self.data['constant_splitting']:
            score += 5
        if self.data['dynamic_calculation']:
            score += 8
        if self.data['encoding_table']:
            score += 10
        if self.data['string_encryption']:
            score += 12
        
        # 指令级混淆评分
        if self.instruction['garbage_injection']:
            score += 5
        if self.instruction['instruction_substitution']:
            score += 8
        if self.instruction['register_allocation']:
            score += 10
        
        # 结构级混淆评分
        if self.structure['function_splitting']:
            score += 8
        if self.structure['function_merging']:
            score += 10
        if self.structure['call_graph_obfuscation']:
            score += 12
        
        # 虚拟化评分
        if self.virtualization['enabled']:
            score += 20
        if self.virtualization['bytecode_vm']:
            score += 15
        if self.virtualization['interpreted_execution']:
            score += 10
        
        # 运行时保护评分
        if self.runtime['debugger_detection']:
            score += 8
        if self.runtime['memory_integrity']:
            score += 10
        if self.runtime['timing_detection']:
            score += 8
        if self.runtime['environment_binding']:
            score += 12
        if self.runtime['anti_tampering']:
            score += 15
        
        # 归一化到0-100
        return min(100, score)
    
    def get_performance_impact(self):
        """计算性能影响
        
        Returns:
            float: 性能影响评分（0-100，越高影响越大）
        """
        impact = 0.0
        
        # 控制流混淆影响
        if self.control_flow['flattening']:
            impact += 20
        if self.control_flow['fake_branches']:
            impact += 5
        if self.control_flow['exception_flow']:
            impact += 15
        if self.control_flow['loop_transform']:
            impact += 10
        
        # 数据混淆影响
        if self.data['constant_splitting']:
            impact += 5
        if self.data['dynamic_calculation']:
            impact += 10
        if self.data['encoding_table']:
            impact += 8
        if self.data['string_encryption']:
            impact += 12
        
        # 指令级混淆影响
        if self.instruction['garbage_injection']:
            impact += 10
        if self.instruction['instruction_substitution']:
            impact += 8
        if self.instruction['register_allocation']:
            impact += 12
        
        # 结构级混淆影响
        if self.structure['function_splitting']:
            impact += 10
        if self.structure['function_merging']:
            impact += 12
        if self.structure['call_graph_obfuscation']:
            impact += 15
        
        # 虚拟化影响
        if self.virtualization['enabled']:
            impact += 30
        if self.virtualization['bytecode_vm']:
            impact += 25
        if self.virtualization['interpreted_execution']:
            impact += 20
        
        # 运行时保护影响
        if self.runtime['debugger_detection']:
            impact += 5
        if self.runtime['memory_integrity']:
            impact += 15
        if self.runtime['timing_detection']:
            impact += 10
        if self.runtime['environment_binding']:
            impact += 8
        if self.runtime['anti_tampering']:
            impact += 12
        
        # 归一化到0-100
        return min(100, impact)
