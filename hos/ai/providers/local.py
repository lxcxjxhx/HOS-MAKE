"""Local provider implementation"""

import random
from typing import Dict, Any, Optional
from hos.ai.providers.base import AIProvider, AIProviderFactory


class LocalProvider(AIProvider):
    """Local provider using heuristic methods for strategy generation"""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize local provider
        
        Args:
            api_key: Not used for local provider
            config: Additional configuration
        """
        super().__init__(api_key, config)
        self.random_seed = self.config.get('random_seed', None)
        if self.random_seed:
            random.seed(self.random_seed)
    
    def generate_strategy(self, code_analysis: Dict[str, Any], performance_mode: str = 'balanced') -> Dict[str, Any]:
        """Generate confusion strategy using heuristic methods
        
        Args:
            code_analysis: Code analysis results
            performance_mode: Performance mode
            
        Returns:
            Dict[str, Any]: Generated strategy configuration
        """
        strategy = self._generate_heuristic_strategy(code_analysis, performance_mode)
        self._add_randomness(strategy)
        return strategy
    
    def is_available(self) -> bool:
        """Check if local provider is available
        
        Returns:
            bool: Always True since it's local
        """
        return True
    
    def _generate_heuristic_strategy(self, code_analysis: Dict[str, Any], performance_mode: str) -> Dict[str, Any]:
        """Generate strategy using heuristic methods
        
        Args:
            code_analysis: Code analysis results
            performance_mode: Performance mode
            
        Returns:
            Dict[str, Any]: Generated strategy
        """
        # Base strategy
        strategy = {
            "control_flow": {
                "flattening": True,
                "fake_branches": True,
                "strength": 0.5
            },
            "data": {
                "constant_splitting": True,
                "dynamic_calculation": True,
                "string_encryption": True,
                "encoding_table": True,
                "strength": 0.5
            },
            "instruction": {
                "garbage_injection": True,
                "instruction_substitution": True,
                "strength": 0.5
            },
            "structure": {
                "function_splitting": True,
                "function_merging": True,
                "call_graph_obfuscation": True,
                "strength": 0.5
            },
            "virtualization": {
                "enabled": False,
                "bytecode_vm": False,
                "strength": 0.0
            },
            "performance": {
                "auto_balance": True,
                "hot_path_protection": True,
                "max_instruction_expansion": 2.0,
                "max_function_overhead": 1.5
            }
        }
        
        # Adjust based on performance mode
        if performance_mode == 'performance':
            base_strength = 0.3
            strategy['virtualization']['enabled'] = False
        elif performance_mode == 'security':
            base_strength = 0.8
            strategy['virtualization']['enabled'] = True
        else:  # balanced
            base_strength = 0.5
        
        # Set base strength
        for key in strategy:
            if isinstance(strategy[key], dict) and 'strength' in strategy[key]:
                strategy[key]['strength'] = base_strength
        
        # Adjust based on code analysis
        if code_analysis:
            # Based on security score
            security_score = code_analysis.get('security_score', 50)
            if security_score > 80:
                for key in strategy:
                    if isinstance(strategy[key], dict) and 'strength' in strategy[key]:
                        strategy[key]['strength'] = min(1.0, strategy[key]['strength'] * 1.2)
            elif security_score < 30:
                for key in strategy:
                    if isinstance(strategy[key], dict) and 'strength' in strategy[key]:
                        strategy[key]['strength'] = max(0.1, strategy[key]['strength'] * 0.8)
            
            # Based on hot paths
            hot_paths = code_analysis.get('hot_paths', [])
            if len(hot_paths) > 2:
                strategy['performance']['hot_path_protection'] = True
                strategy['control_flow']['strength'] *= 0.8
                strategy['instruction']['strength'] *= 0.8
            
            # Based on code size
            code_size = code_analysis.get('code_size', 0)
            line_count = code_analysis.get('line_count', 0)
            if code_size > 10000 or line_count > 500:
                strategy['performance']['max_instruction_expansion'] = 1.5
                strategy['performance']['max_function_overhead'] = 1.2
            elif code_size < 1000 or line_count < 50:
                strategy['performance']['max_instruction_expansion'] = 2.5
                strategy['performance']['max_function_overhead'] = 1.8
            
            # Based on sensitivity
            sensitivity = code_analysis.get('sensitivity', {})
            sensitivity_score = sensitivity.get('sensitivity_score', 0)
            if sensitivity_score > 70:
                strategy['data']['constant_splitting'] = True
                strategy['data']['dynamic_calculation'] = True
                strategy['data']['string_encryption'] = True
                strategy['data']['encoding_table'] = True
                strategy['data']['strength'] = min(1.0, strategy['data']['strength'] * 1.2)
            
            # Based on function count
            function_count = len(code_analysis.get('ast', {}).get('functions', []))
            if function_count > 20:
                strategy['structure']['function_splitting'] = True
                strategy['structure']['call_graph_obfuscation'] = True
            elif function_count < 5:
                strategy['structure']['function_splitting'] = False
                strategy['structure']['function_merging'] = False
            
            # Based on class count
            class_count = len(code_analysis.get('ast', {}).get('classes', []))
            if class_count > 10 and performance_mode != 'performance':
                strategy['virtualization']['enabled'] = True
                strategy['virtualization']['bytecode_vm'] = True
        
        return strategy
    
    def _add_randomness(self, strategy: Dict[str, Any]):
        """Add randomness to strategy
        
        Args:
            strategy: Strategy to modify
        """
        # Randomly adjust control flow
        if random.random() > 0.7:
            strategy['control_flow']['flattening'] = not strategy['control_flow']['flattening']
        if random.random() > 0.6:
            strategy['control_flow']['fake_branches'] = not strategy['control_flow']['fake_branches']
        
        # Randomly adjust data
        if random.random() > 0.7:
            strategy['data']['dynamic_calculation'] = not strategy['data']['dynamic_calculation']
        if random.random() > 0.6:
            strategy['data']['encoding_table'] = not strategy['data']['encoding_table']
        
        # Randomly adjust instruction
        if random.random() > 0.7:
            strategy['instruction']['garbage_injection'] = not strategy['instruction']['garbage_injection']
        
        # Randomly adjust structure
        if random.random() > 0.8:
            strategy['structure']['function_merging'] = not strategy['structure']['function_merging']
        
        # Randomly adjust virtualization
        if random.random() > 0.9 and strategy['virtualization']['enabled']:
            strategy['virtualization']['bytecode_vm'] = not strategy['virtualization']['bytecode_vm']


# Register provider
AIProviderFactory.register_provider('local', LocalProvider)
