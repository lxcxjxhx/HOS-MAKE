"""AI策略生成器"""

import json
import random
from hos.ai.strategy import ConfusionStrategy
from hos.ai.dataset import StrategyDataset
from hos.ai.providers import AIProviderFactory

class AIStrategyGenerator:
    """AI策略生成器"""
    
    def __init__(self, model_path=None, provider='local', api_key=None, provider_config=None):
        """初始化AI策略生成器
        
        Args:
            model_path: 模型路径（可选）
            provider: AI provider name ('local', 'openai', 'anthropic', 'google')
            api_key: API key for the provider
            provider_config: Additional provider configuration
        """
        self.model_path = model_path
        self.dataset = StrategyDataset()
        self.trained = False
        
        # 初始化AI provider
        self.provider_name = provider
        self.api_key = api_key
        self.provider_config = provider_config or {}
        self.provider = AIProviderFactory.create_provider(
            provider, api_key, self.provider_config
        )
        
        # 模拟模型加载
        if model_path:
            print(f"Loading model from {model_path}...")
            # 实际实现中，这里应该加载预训练的模型
            self.trained = True
    
    def train(self, dataset=None, epochs=10):
        """训练模型
        
        Args:
            dataset: 训练数据集（可选）
            epochs: 训练轮数
            
        Returns:
            bool: 训练是否成功
        """
        if not dataset:
            # 如果没有提供数据集，生成一个
            dataset = self.dataset.generate_dataset(size=1000)
        
        # 模拟训练过程
        print(f"Training model with {len(dataset)} samples for {epochs} epochs...")
        for epoch in range(epochs):
            print(f"Epoch {epoch+1}/{epochs}...")
            # 实际实现中，这里应该执行模型训练
        
        self.trained = True
        print("Training completed successfully!")
        return True
    
    def generate_strategy(self, code_analysis=None, performance_mode='balanced'):
        """生成混淆策略
        
        Args:
            code_analysis: 代码分析结果（可选）
            performance_mode: 性能模式（'balanced', 'performance', 'security'）
            
        Returns:
            ConfusionStrategy: 生成的混淆策略
        """
        # 使用AI provider生成策略
        if self.provider.is_available():
            try:
                strategy_dict = self.provider.generate_strategy(code_analysis, performance_mode)
                strategy = ConfusionStrategy()
                strategy.from_dict(strategy_dict)
                return strategy
            except Exception as e:
                print(f"Error using AI provider: {e}")
                # Fallback to heuristic method
                return self._generate_heuristic_strategy(code_analysis, performance_mode)
        else:
            # Fallback to heuristic method if provider is not available
            return self._generate_heuristic_strategy(code_analysis, performance_mode)
    
    def _generate_heuristic_strategy(self, code_analysis, performance_mode):
        """使用启发式方法生成策略
        
        Args:
            code_analysis: 代码分析结果
            performance_mode: 性能模式
            
        Returns:
            ConfusionStrategy: 生成的混淆策略
        """
        strategy = ConfusionStrategy()
        
        # 设置性能模式
        strategy.set_performance_mode(performance_mode)
        
        # 根据代码分析结果调整策略
        if code_analysis:
            # 基于安全评分调整强度
            security_score = code_analysis.get('security_score', 50)
            
            # 基于性能模式和安全评分调整强度
            if performance_mode == 'performance':
                base_strength = 0.3
                if security_score > 80:
                    strength = min(0.5, base_strength + 0.2)
                else:
                    strength = base_strength
            elif performance_mode == 'security':
                base_strength = 0.8
                if security_score < 30:
                    strength = max(0.6, base_strength - 0.2)
                else:
                    strength = base_strength
            else:  # balanced
                if security_score > 80:
                    strength = 0.7
                elif security_score > 50:
                    strength = 0.5
                else:
                    strength = 0.4
            
            strategy.set_strength(strength)
            
            # 基于热路径调整性能控制
            hot_paths = code_analysis.get('hot_paths', [])
            if len(hot_paths) > 2:
                strategy.performance['hot_path_protection'] = True
                # 降低热路径的混淆强度
                strategy.control_flow['strength'] *= 0.8
                strategy.instruction['strength'] *= 0.8
            
            # 基于代码大小调整指令膨胀率
            code_size = code_analysis.get('code_size', 0)
            line_count = code_analysis.get('line_count', 0)
            
            if code_size > 10000 or line_count > 500:
                # 大型代码，限制指令膨胀
                strategy.performance['max_instruction_expansion'] = 1.5
                strategy.performance['max_function_overhead'] = 1.2
            elif code_size < 1000 or line_count < 50:
                # 小型代码，可以增加指令膨胀
                strategy.performance['max_instruction_expansion'] = 2.5
                strategy.performance['max_function_overhead'] = 1.8
            
            # 基于敏感度分析调整数据混淆
            sensitivity = code_analysis.get('sensitivity', {})
            sensitivity_score = sensitivity.get('sensitivity_score', 0)
            
            if sensitivity_score > 70:
                # 高敏感度代码，加强数据混淆
                strategy.data['constant_splitting'] = True
                strategy.data['dynamic_calculation'] = True
                strategy.data['string_encryption'] = True
                strategy.data['encoding_table'] = True
                strategy.data['strength'] = min(1.0, strategy.data['strength'] * 1.2)
            
            # 基于函数数量调整结构混淆
            function_count = len(code_analysis.get('ast', {}).get('functions', []))
            if function_count > 20:
                # 函数数量多，加强结构混淆
                strategy.structure['function_splitting'] = True
                strategy.structure['call_graph_obfuscation'] = True
            elif function_count < 5:
                # 函数数量少，避免过度拆分
                strategy.structure['function_splitting'] = False
                strategy.structure['function_merging'] = False
            
            # 基于类数量调整虚拟化
            class_count = len(code_analysis.get('ast', {}).get('classes', []))
            if class_count > 10 and performance_mode != 'performance':
                # 类数量多，考虑启用虚拟化
                strategy.virtualization['enabled'] = True
                strategy.virtualization['bytecode_vm'] = True
        
        # 添加一些随机性，确保每个策略都是唯一的
        self._add_randomness(strategy)
        
        return strategy
    
    def _add_randomness(self, strategy):
        """添加随机性到策略中
        
        Args:
            strategy: 混淆策略
        """
        # 随机调整控制流混淆
        if random.random() > 0.7:
            strategy.control_flow['flattening'] = not strategy.control_flow['flattening']
        if random.random() > 0.6:
            strategy.control_flow['fake_branches'] = not strategy.control_flow['fake_branches']
        
        # 随机调整数据混淆
        if random.random() > 0.7:
            strategy.data['dynamic_calculation'] = not strategy.data['dynamic_calculation']
        if random.random() > 0.6:
            strategy.data['encoding_table'] = not strategy.data['encoding_table']
        
        # 随机调整指令级混淆
        if random.random() > 0.7:
            strategy.instruction['garbage_injection'] = not strategy.instruction['garbage_injection']
        
        # 随机调整结构级混淆
        if random.random() > 0.8:
            strategy.structure['function_merging'] = not strategy.structure['function_merging']
        
        # 随机调整运行时保护
        if random.random() > 0.6:
            strategy.runtime['timing_detection'] = not strategy.runtime['timing_detection']
        if random.random() > 0.8:
            strategy.runtime['anti_tampering'] = not strategy.runtime['anti_tampering']
    
    def evaluate_strategy(self, strategy, code_analysis=None):
        """评估策略
        
        Args:
            strategy: 要评估的策略
            code_analysis: 代码分析结果（可选）
            
        Returns:
            dict: 评估结果
        """
        # 计算安全评分
        security_score = strategy.get_security_score()
        
        # 计算性能影响
        performance_impact = strategy.get_performance_impact()
        
        # 计算平衡评分
        balance_score = self._calculate_balance_score(security_score, performance_impact, strategy.performance['auto_balance'])
        
        # 评估策略有效性
        validity = strategy.validate()
        
        # 基于代码分析结果调整评估
        if code_analysis:
            # 检查策略是否适合代码复杂度
            code_complexity = code_analysis.get('line_count', 0)
            if code_complexity > 1000 and security_score < 50:
                security_score -= 10
            elif code_complexity < 100 and security_score > 80:
                performance_impact += 10
        
        return {
            'security_score': security_score,
            'performance_impact': performance_impact,
            'balance_score': balance_score,
            'valid': validity,
            'recommendations': self._generate_recommendations(strategy, security_score, performance_impact)
        }
    
    def _calculate_balance_score(self, security_score, performance_impact, auto_balance):
        """计算平衡评分
        
        Args:
            security_score: 安全评分
            performance_impact: 性能影响
            auto_balance: 是否自动平衡
            
        Returns:
            float: 平衡评分（0-100）
        """
        if auto_balance:
            # 自动平衡模式下，追求安全和性能的平衡
            ideal_security = 70
            ideal_performance = 30
            
            security_diff = abs(security_score - ideal_security)
            performance_diff = abs(performance_impact - ideal_performance)
            
            # 计算平衡评分
            balance_score = 100 - (security_diff + performance_diff) / 2
        else:
            # 非自动平衡模式下，根据性能模式计算
            # 这里简化处理
            balance_score = (security_score + (100 - performance_impact)) / 2
        
        return max(0, min(100, balance_score))
    
    def _generate_recommendations(self, strategy, security_score, performance_impact):
        """生成策略建议
        
        Args:
            strategy: 混淆策略
            security_score: 安全评分
            performance_impact: 性能影响
            
        Returns:
            list: 建议列表
        """
        recommendations = []
        
        if security_score < 50:
            recommendations.append("建议增加混淆强度，特别是控制流平坦化和数据混淆")
            recommendations.append("考虑启用字符串加密和运行时保护")
        
        if performance_impact > 70:
            recommendations.append("建议降低混淆强度，特别是虚拟化和控制流平坦化")
            recommendations.append("启用热路径保护以提高性能")
        
        if security_score > 80 and performance_impact < 30:
            recommendations.append("策略平衡良好，继续保持")
        
        if not strategy.virtualization['enabled'] and security_score < 70:
            recommendations.append("考虑启用虚拟化以提高安全性")
        
        if strategy.performance['hot_path_protection'] and len(recommendations) == 0:
            recommendations.append("策略配置合理，无需调整")
        
        return recommendations
    
    def save_model(self, path):
        """保存模型
        
        Args:
            path: 保存路径
            
        Returns:
            bool: 保存是否成功
        """
        # 模拟保存模型
        print(f"Saving model to {path}...")
        # 实际实现中，这里应该保存模型权重和配置
        return True
    
    def load_model(self, path):
        """加载模型
        
        Args:
            path: 模型路径
            
        Returns:
            bool: 加载是否成功
        """
        # 模拟加载模型
        print(f"Loading model from {path}...")
        # 实际实现中，这里应该加载模型权重和配置
        self.trained = True
        return True
