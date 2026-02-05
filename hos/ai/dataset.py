"""策略数据集类"""

import json
import os
import random
from hos.ai.strategy import ConfusionStrategy

class StrategyDataset:
    """策略数据集"""
    
    def __init__(self, data_dir=None):
        """初始化策略数据集
        
        Args:
            data_dir: 数据目录（可选）
        """
        self.data_dir = data_dir
        self.strategies = []
        
        if data_dir and os.path.exists(data_dir):
            self.load_from_dir(data_dir)
    
    def generate_sample(self, code_analysis=None):
        """生成一个策略样本
        
        Args:
            code_analysis: 代码分析结果（可选）
            
        Returns:
            ConfusionStrategy: 混淆策略
        """
        strategy = ConfusionStrategy()
        
        # 根据代码分析结果调整策略
        if code_analysis:
            # 基于安全评分调整强度
            security_score = code_analysis.get('security_score', 50)
            if security_score > 80:
                strategy.set_strength(random.uniform(0.7, 0.9))
            elif security_score > 50:
                strategy.set_strength(random.uniform(0.5, 0.7))
            else:
                strategy.set_strength(random.uniform(0.3, 0.5))
            
            # 基于热路径调整性能控制
            hot_path_count = len(code_analysis.get('hot_paths', []))
            if hot_path_count > 2:
                strategy.performance['hot_path_protection'] = True
            
            # 基于代码大小调整指令膨胀率
            code_size = code_analysis.get('code_size', 0)
            if code_size > 10000:
                strategy.performance['max_instruction_expansion'] = random.uniform(1.2, 1.5)
            elif code_size > 5000:
                strategy.performance['max_instruction_expansion'] = random.uniform(1.5, 2.0)
            else:
                strategy.performance['max_instruction_expansion'] = random.uniform(2.0, 2.5)
        else:
            # 随机生成策略
            strength = random.uniform(0.3, 0.8)
            strategy.set_strength(strength)
            
            # 随机设置性能模式
            performance_modes = ['balanced', 'performance', 'security']
            mode = random.choice(performance_modes)
            strategy.set_performance_mode(mode)
        
        # 随机调整一些参数以增加多样性
        self._randomize_strategy(strategy)
        
        return strategy
    
    def _randomize_strategy(self, strategy):
        """随机化策略参数
        
        Args:
            strategy: 混淆策略
        """
        # 随机调整控制流混淆
        if random.random() > 0.5:
            strategy.control_flow['flattening'] = not strategy.control_flow['flattening']
        if random.random() > 0.5:
            strategy.control_flow['fake_branches'] = not strategy.control_flow['fake_branches']
        if random.random() > 0.7:
            strategy.control_flow['exception_flow'] = not strategy.control_flow['exception_flow']
        
        # 随机调整数据混淆
        if random.random() > 0.5:
            strategy.data['constant_splitting'] = not strategy.data['constant_splitting']
        if random.random() > 0.5:
            strategy.data['dynamic_calculation'] = not strategy.data['dynamic_calculation']
        if random.random() > 0.7:
            strategy.data['string_encryption'] = not strategy.data['string_encryption']
        
        # 随机调整指令级混淆
        if random.random() > 0.5:
            strategy.instruction['garbage_injection'] = not strategy.instruction['garbage_injection']
        if random.random() > 0.7:
            strategy.instruction['instruction_substitution'] = not strategy.instruction['instruction_substitution']
        
        # 随机调整结构级混淆
        if random.random() > 0.7:
            strategy.structure['function_splitting'] = not strategy.structure['function_splitting']
        if random.random() > 0.8:
            strategy.structure['function_merging'] = not strategy.structure['function_merging']
        
        # 随机调整虚拟化
        if random.random() > 0.8:
            strategy.virtualization['enabled'] = not strategy.virtualization['enabled']
            if strategy.virtualization['enabled']:
                strategy.virtualization['bytecode_vm'] = random.random() > 0.5
                strategy.virtualization['interpreted_execution'] = random.random() > 0.5
        
        # 随机调整运行时保护
        if random.random() > 0.5:
            strategy.runtime['debugger_detection'] = not strategy.runtime['debugger_detection']
        if random.random() > 0.7:
            strategy.runtime['memory_integrity'] = not strategy.runtime['memory_integrity']
        if random.random() > 0.8:
            strategy.runtime['environment_binding'] = not strategy.runtime['environment_binding']
    
    def generate_dataset(self, size=1000, code_analyses=None):
        """生成数据集
        
        Args:
            size: 数据集大小
            code_analyses: 代码分析结果列表（可选）
            
        Returns:
            list: 策略列表
        """
        dataset = []
        
        for i in range(size):
            if code_analyses and i < len(code_analyses):
                strategy = self.generate_sample(code_analyses[i])
            else:
                strategy = self.generate_sample()
            
            # 计算安全评分和性能影响
            security_score = strategy.get_security_score()
            performance_impact = strategy.get_performance_impact()
            
            # 添加到数据集
            dataset.append({
                'strategy': strategy.to_dict(),
                'security_score': security_score,
                'performance_impact': performance_impact,
                'metadata': {
                    'id': i,
                    'timestamp': i,  # 简化版，实际应该使用时间戳
                    'source': 'generated'
                }
            })
        
        self.strategies.extend(dataset)
        return dataset
    
    def save_to_dir(self, output_dir):
        """保存数据集到目录
        
        Args:
            output_dir: 输出目录
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for i, item in enumerate(self.strategies):
            filename = os.path.join(output_dir, f'strategy_{i}.json')
            with open(filename, 'w') as f:
                json.dump(item, f, indent=2)
    
    def load_from_dir(self, input_dir):
        """从目录加载数据集
        
        Args:
            input_dir: 输入目录
        """
        for filename in os.listdir(input_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(input_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        item = json.load(f)
                        self.strategies.append(item)
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
    
    def get_statistics(self):
        """获取数据集统计信息
        
        Returns:
            dict: 统计信息
        """
        if not self.strategies:
            return {}
        
        security_scores = []
        performance_impacts = []
        strength_values = []
        
        for item in self.strategies:
            security_scores.append(item.get('security_score', 0))
            performance_impacts.append(item.get('performance_impact', 0))
            strength = item.get('strategy', {}).get('control_flow', {}).get('strength', 0)
            strength_values.append(strength)
        
        return {
            'total_samples': len(self.strategies),
            'avg_security_score': sum(security_scores) / len(security_scores),
            'avg_performance_impact': sum(performance_impacts) / len(performance_impacts),
            'avg_strength': sum(strength_values) / len(strength_values),
            'min_security_score': min(security_scores),
            'max_security_score': max(security_scores),
            'min_performance_impact': min(performance_impacts),
            'max_performance_impact': max(performance_impacts)
        }
    
    def split_dataset(self, train_ratio=0.8, val_ratio=0.1):
        """分割数据集
        
        Args:
            train_ratio: 训练集比例
            val_ratio: 验证集比例
            
        Returns:
            tuple: (训练集, 验证集, 测试集)
        """
        import random
        
        # 随机打乱数据集
        random.shuffle(self.strategies)
        
        # 计算分割点
        total = len(self.strategies)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)
        
        # 分割数据集
        train_set = self.strategies[:train_end]
        val_set = self.strategies[train_end:val_end]
        test_set = self.strategies[val_end:]
        
        return train_set, val_set, test_set
