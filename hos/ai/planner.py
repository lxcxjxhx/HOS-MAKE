"""策略规划器模块"""

from hos.ai.strategy import ConfusionStrategy
from hos.ai.model import AIStrategyGenerator

class StrategyPlanner:
    """策略规划器"""
    
    def __init__(self):
        """初始化策略规划器"""
        self.ai_generator = AIStrategyGenerator()
    
    def plan_strategy(self, code_analysis, performance_mode='balanced', security_level='medium'):
        """规划混淆策略
        
        Args:
            code_analysis: 代码分析结果
            performance_mode: 性能模式（'balanced', 'performance', 'security'）
            security_level: 安全级别（'low', 'medium', 'high'）
            
        Returns:
            dict: 策略规划结果，包含混淆策略和评估
        """
        # 提取输入特征
        features = self._extract_features(code_analysis)
        
        # 生成混淆策略
        strategy = self._generate_strategy(features, performance_mode, security_level)
        
        # 评估策略
        evaluation = self._evaluate_strategy(strategy, code_analysis)
        
        # 优化策略
        optimized_strategy = self._optimize_strategy(strategy, evaluation, code_analysis)
        
        # 再次评估优化后的策略
        optimized_evaluation = self._evaluate_strategy(optimized_strategy, code_analysis)
        
        return {
            'strategy': optimized_strategy,
            'evaluation': optimized_evaluation,
            'features': features
        }
    
    def _extract_features(self, code_analysis):
        """提取输入特征
        
        Args:
            code_analysis: 代码分析结果
            
        Returns:
            dict: 提取的特征
        """
        features = {}
        
        # 代码结构特征
        features['code_size'] = code_analysis.get('code_size', 0)
        features['line_count'] = code_analysis.get('line_count', 0)
        features['function_count'] = len(code_analysis.get('ast', {}).get('functions', []))
        features['class_count'] = len(code_analysis.get('ast', {}).get('classes', []))
        features['import_count'] = len(code_analysis.get('ast', {}).get('imports', []))
        
        # 控制流特征
        features['hot_path_count'] = len(code_analysis.get('hot_paths', []))
        
        # 数据流特征
        data_flow = code_analysis.get('data_flow', {})
        features['live_variables'] = len(data_flow.get('live_variables', {}).get('in_sets', {}))
        
        # 敏感度特征
        sensitivity = code_analysis.get('sensitivity', {})
        features['sensitivity_score'] = sensitivity.get('sensitivity_score', 0)
        features['sensitive_strings_count'] = len(sensitivity.get('sensitive_strings', []))
        features['sensitive_constants_count'] = len(sensitivity.get('sensitive_constants', []))
        features['sensitive_functions_count'] = len(sensitivity.get('sensitive_functions', []))
        features['sensitive_variables_count'] = len(sensitivity.get('sensitive_variables', []))
        
        # 安全价值特征
        features['security_score'] = code_analysis.get('security_score', 0)
        
        return features
    
    def _generate_strategy(self, features, performance_mode, security_level):
        """生成混淆策略
        
        Args:
            features: 输入特征
            performance_mode: 性能模式
            security_level: 安全级别
            
        Returns:
            ConfusionStrategy: 生成的混淆策略
        """
        # 使用AI生成策略
        strategy = self.ai_generator.generate_strategy(None, performance_mode)
        
        # 根据安全级别调整强度
        if security_level == 'low':
            strategy.set_strength(0.3)
        elif security_level == 'medium':
            strategy.set_strength(0.5)
        else:  # high
            strategy.set_strength(0.8)
        
        # 根据特征调整策略
        self._adjust_strategy_by_features(strategy, features)
        
        return strategy
    
    def _adjust_strategy_by_features(self, strategy, features):
        """根据特征调整策略
        
        Args:
            strategy: 混淆策略
            features: 输入特征
        """
        # 基于代码大小调整
        code_size = features.get('code_size', 0)
        if code_size > 10000:
            # 大型代码，限制指令膨胀
            strategy.performance['max_instruction_expansion'] = 1.5
        elif code_size < 1000:
            # 小型代码，可以增加指令膨胀
            strategy.performance['max_instruction_expansion'] = 2.5
        
        # 基于函数数量调整
        function_count = features.get('function_count', 0)
        if function_count > 20:
            # 函数数量多，加强结构混淆
            strategy.structure['function_splitting'] = True
            strategy.structure['call_graph_obfuscation'] = True
        elif function_count < 5:
            # 函数数量少，避免过度拆分
            strategy.structure['function_splitting'] = False
            strategy.structure['function_merging'] = False
        
        # 基于热路径数量调整
        hot_path_count = features.get('hot_path_count', 0)
        if hot_path_count > 2:
            # 有多个热路径，启用热路径保护
            strategy.performance['hot_path_protection'] = True
            # 降低热路径的混淆强度
            strategy.control_flow['strength'] *= 0.8
            strategy.instruction['strength'] *= 0.8
        
        # 基于敏感度调整
        sensitivity_score = features.get('sensitivity_score', 0)
        if sensitivity_score > 70:
            # 高敏感度，加强数据混淆
            strategy.data['constant_splitting'] = True
            strategy.data['dynamic_calculation'] = True
            strategy.data['string_encryption'] = True
            strategy.data['encoding_table'] = True
        
        # 基于安全评分调整
        security_score = features.get('security_score', 0)
        if security_score > 80:
            # 高安全价值，加强保护
            strategy.virtualization['enabled'] = True
            strategy.virtualization['bytecode_vm'] = True
            strategy.runtime['debugger_detection'] = True
            strategy.runtime['memory_integrity'] = True
        elif security_score < 30:
            # 低安全价值，减少保护以提高性能
            strategy.virtualization['enabled'] = False
            strategy.runtime['debugger_detection'] = False
    
    def _evaluate_strategy(self, strategy, code_analysis):
        """评估策略
        
        Args:
            strategy: 混淆策略
            code_analysis: 代码分析结果
            
        Returns:
            dict: 评估结果
        """
        # 使用AI模型评估策略
        evaluation = self.ai_generator.evaluate_strategy(strategy, code_analysis)
        
        # 添加额外的评估指标
        evaluation['complexity'] = self._calculate_strategy_complexity(strategy)
        evaluation['coverage'] = self._calculate_strategy_coverage(strategy)
        evaluation['feasibility'] = self._calculate_strategy_feasibility(strategy, code_analysis)
        
        return evaluation
    
    def _calculate_strategy_complexity(self, strategy):
        """计算策略复杂度
        
        Args:
            strategy: 混淆策略
            
        Returns:
            float: 复杂度评分（0-100）
        """
        complexity = 0
        
        # 控制流复杂度
        if strategy.control_flow.get('flattening', False):
            complexity += 20
        if strategy.control_flow.get('fake_branches', False):
            complexity += 10
        if strategy.control_flow.get('exception_flow', False):
            complexity += 15
        if strategy.control_flow.get('loop_transform', False):
            complexity += 10
        
        # 数据复杂度
        if strategy.data.get('constant_splitting', False):
            complexity += 10
        if strategy.data.get('dynamic_calculation', False):
            complexity += 15
        if strategy.data.get('encoding_table', False):
            complexity += 15
        if strategy.data.get('string_encryption', False):
            complexity += 15
        
        # 指令复杂度
        if strategy.instruction.get('garbage_injection', False):
            complexity += 10
        if strategy.instruction.get('instruction_substitution', False):
            complexity += 10
        if strategy.instruction.get('register_allocation', False):
            complexity += 10
        
        # 结构复杂度
        if strategy.structure.get('function_splitting', False):
            complexity += 15
        if strategy.structure.get('function_merging', False):
            complexity += 15
        if strategy.structure.get('call_graph_obfuscation', False):
            complexity += 15
        
        # 虚拟化复杂度
        if strategy.virtualization.get('enabled', False):
            complexity += 25
        
        # 运行时保护复杂度
        if strategy.runtime.get('debugger_detection', False):
            complexity += 10
        if strategy.runtime.get('memory_integrity', False):
            complexity += 15
        if strategy.runtime.get('timing_detection', False):
            complexity += 10
        if strategy.runtime.get('environment_binding', False):
            complexity += 15
        if strategy.runtime.get('anti_tampering', False):
            complexity += 15
        
        return min(100, complexity)
    
    def _calculate_strategy_coverage(self, strategy):
        """计算策略覆盖率
        
        Args:
            strategy: 混淆策略
            
        Returns:
            float: 覆盖率评分（0-100）
        """
        coverage = 0
        
        # 控制流覆盖
        control_flow_features = ['flattening', 'fake_branches', 'exception_flow', 'loop_transform']
        control_flow_enabled = sum(1 for feature in control_flow_features if strategy.control_flow.get(feature, False))
        coverage += (control_flow_enabled / len(control_flow_features)) * 25
        
        # 数据覆盖
        data_features = ['constant_splitting', 'dynamic_calculation', 'encoding_table', 'string_encryption']
        data_enabled = sum(1 for feature in data_features if strategy.data.get(feature, False))
        coverage += (data_enabled / len(data_features)) * 25
        
        # 指令覆盖
        instruction_features = ['garbage_injection', 'instruction_substitution', 'register_allocation']
        instruction_enabled = sum(1 for feature in instruction_features if strategy.instruction.get(feature, False))
        coverage += (instruction_enabled / len(instruction_features)) * 15
        
        # 结构覆盖
        structure_features = ['function_splitting', 'function_merging', 'call_graph_obfuscation']
        structure_enabled = sum(1 for feature in structure_features if strategy.structure.get(feature, False))
        coverage += (structure_enabled / len(structure_features)) * 15
        
        # 虚拟化覆盖
        virtualization_features = ['enabled']
        virtualization_enabled = sum(1 for feature in virtualization_features if strategy.virtualization.get(feature, False))
        coverage += (virtualization_enabled / len(virtualization_features)) * 10
        
        # 运行时保护覆盖
        runtime_features = ['debugger_detection', 'memory_integrity', 'timing_detection', 'environment_binding', 'anti_tampering']
        runtime_enabled = sum(1 for feature in runtime_features if strategy.runtime.get(feature, False))
        coverage += (runtime_enabled / len(runtime_features)) * 10
        
        return min(100, coverage)
    
    def _calculate_strategy_feasibility(self, strategy, code_analysis):
        """计算策略可行性
        
        Args:
            strategy: 混淆策略
            code_analysis: 代码分析结果
            
        Returns:
            float: 可行性评分（0-100）
        """
        feasibility = 100
        
        # 基于代码大小评估
        code_size = code_analysis.get('code_size', 0)
        if code_size > 10000:
            # 大型代码，检查虚拟化可行性
            if strategy.virtualization.get('enabled', False):
                feasibility -= 20
        
        # 基于函数数量评估
        function_count = len(code_analysis.get('ast', {}).get('functions', []))
        if function_count > 50:
            # 函数数量多，检查结构变换可行性
            if strategy.structure.get('function_splitting', False) and strategy.structure.get('function_merging', False):
                feasibility -= 15
        
        # 基于热路径数量评估
        hot_path_count = len(code_analysis.get('hot_paths', []))
        if hot_path_count > 3:
            # 热路径多，检查控制流变换可行性
            if strategy.control_flow.get('flattening', False):
                feasibility -= 10
        
        # 基于敏感度评估
        sensitivity_score = code_analysis.get('sensitivity', {}).get('sensitivity_score', 0)
        if sensitivity_score > 80:
            # 高敏感度，检查数据变换可行性
            if not strategy.data.get('string_encryption', False):
                feasibility -= 20
        
        return max(0, feasibility)
    
    def _optimize_strategy(self, strategy, evaluation, code_analysis):
        """优化策略
        
        Args:
            strategy: 混淆策略
            evaluation: 策略评估结果
            code_analysis: 代码分析结果
            
        Returns:
            ConfusionStrategy: 优化后的策略
        """
        optimized_strategy = ConfusionStrategy()
        optimized_strategy.from_dict(strategy.to_dict())
        
        # 基于评估结果优化
        security_score = evaluation.get('security_score', 0)
        performance_impact = evaluation.get('performance_impact', 0)
        balance_score = evaluation.get('balance_score', 0)
        feasibility = evaluation.get('feasibility', 0)
        
        # 优化安全性
        if security_score < 60:
            # 提高安全级别
            optimized_strategy.set_strength(min(1.0, optimized_strategy.control_flow['strength'] * 1.2))
            optimized_strategy.control_flow['flattening'] = True
            optimized_strategy.data['string_encryption'] = True
            optimized_strategy.runtime['debugger_detection'] = True
        
        # 优化性能
        if performance_impact > 70:
            # 降低性能影响
            optimized_strategy.set_strength(max(0.3, optimized_strategy.control_flow['strength'] * 0.8))
            optimized_strategy.virtualization['enabled'] = False
            optimized_strategy.control_flow['flattening'] = False
            optimized_strategy.control_flow['exception_flow'] = False
        
        # 优化可行性
        if feasibility < 70:
            # 提高可行性
            if code_analysis.get('code_size', 0) > 10000:
                optimized_strategy.virtualization['enabled'] = False
            if len(code_analysis.get('ast', {}).get('functions', [])) > 50:
                optimized_strategy.structure['function_merging'] = False
            if len(code_analysis.get('hot_paths', [])) > 3:
                optimized_strategy.control_flow['flattening'] = False
        
        # 优化平衡性
        if balance_score < 60:
            # 提高平衡性
            if security_score < performance_impact:
                # 安全性不足，提高安全级别
                optimized_strategy.set_strength(min(1.0, optimized_strategy.control_flow['strength'] * 1.1))
            else:
                # 性能影响过大，降低安全级别
                optimized_strategy.set_strength(max(0.3, optimized_strategy.control_flow['strength'] * 0.9))
        
        return optimized_strategy
