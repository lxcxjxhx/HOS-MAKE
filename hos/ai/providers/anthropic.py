"""Anthropic provider implementation"""

import os
import json
from typing import Dict, Any, Optional
from hos.ai.providers.base import AIProvider, AIProviderFactory


class AnthropicProvider(AIProvider):
    """Anthropic Claude API provider for strategy generation"""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize Anthropic provider
        
        Args:
            api_key: Anthropic API key
            config: Additional configuration
        """
        super().__init__(api_key, config)
        self.model = self.config.get('model', 'claude-3-opus-20240229')
        self.temperature = self.config.get('temperature', 0.3)
        self.max_tokens = self.config.get('max_tokens', 1000)
        self.timeout = self.config.get('timeout', 30)
        
    def generate_strategy(self, code_analysis: Dict[str, Any], performance_mode: str = 'balanced') -> Dict[str, Any]:
        """Generate confusion strategy using Anthropic API
        
        Args:
            code_analysis: Code analysis results
            performance_mode: Performance mode
            
        Returns:
            Dict[str, Any]: Generated strategy configuration
        """
        try:
            import anthropic
            
            # Set API key
            client = anthropic.Anthropic(
                api_key=self.api_key or os.environ.get('ANTHROPIC_API_KEY')
            )
            
            # Create prompt
            prompt = self._create_prompt(code_analysis, performance_mode)
            
            # Call Anthropic API
            response = client.messages.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=self.timeout
            )
            
            # Extract strategy from response
            strategy_content = response.content[0].text
            strategy = self._parse_strategy(strategy_content)
            
            return strategy
            
        except Exception as e:
            # Fallback to default strategy if API call fails
            print(f"Anthropic API error: {e}")
            return self._get_default_strategy(performance_mode)
    
    def is_available(self) -> bool:
        """Check if Anthropic provider is available
        
        Returns:
            bool: True if available, False otherwise
        """
        try:
            import anthropic
            return bool(self.api_key or os.environ.get('ANTHROPIC_API_KEY'))
        except ImportError:
            return False
    
    def _create_prompt(self, code_analysis: Dict[str, Any], performance_mode: str) -> str:
        """Create prompt for Anthropic
        
        Args:
            code_analysis: Code analysis results
            performance_mode: Performance mode
            
        Returns:
            str: Prompt string
        """
        prompt = f"""Generate a comprehensive Python code obfuscation strategy based on the following analysis:

Code Analysis:
- Code size: {code_analysis.get('code_size', 0)} bytes
- Line count: {code_analysis.get('line_count', 0)}
- Function count: {len(code_analysis.get('ast', {}).get('functions', []))}
- Class count: {len(code_analysis.get('ast', {}).get('classes', []))}
- Hot paths: {len(code_analysis.get('hot_paths', []))}
- Sensitivity score: {code_analysis.get('sensitivity', {}).get('sensitivity_score', 0)}
- Security score: {code_analysis.get('security_score', 0)}

Performance Mode: {performance_mode}

Requirements:
1. Generate a JSON object with the following structure:
{
    "control_flow": {
        "flattening": bool,
        "fake_branches": bool,
        "strength": float (0-1)
    },
    "data": {
        "constant_splitting": bool,
        "dynamic_calculation": bool,
        "string_encryption": bool,
        "encoding_table": bool,
        "strength": float (0-1)
    },
    "instruction": {
        "garbage_injection": bool,
        "instruction_substitution": bool,
        "strength": float (0-1)
    },
    "structure": {
        "function_splitting": bool,
        "function_merging": bool,
        "call_graph_obfuscation": bool,
        "strength": float (0-1)
    },
    "virtualization": {
        "enabled": bool,
        "bytecode_vm": bool,
        "strength": float (0-1)
    },
    "performance": {
        "auto_balance": bool,
        "hot_path_protection": bool,
        "max_instruction_expansion": float,
        "max_function_overhead": float
    }
}

2. Adjust the strategy based on performance mode:
   - 'performance': Prioritize speed, use lighter obfuscation
   - 'balanced': Balance security and performance
   - 'security': Maximize security, accept performance impact

3. Consider the code analysis when setting parameters:
   - High sensitivity score: Increase data obfuscation
   - Many functions/classes: Increase structure obfuscation
   - Hot paths: Be conservative with those sections

4. Only return the JSON object, no additional text."""
        
        return prompt
    
    def _parse_strategy(self, content: str) -> Dict[str, Any]:
        """Parse strategy from Anthropic response
        
        Args:
            content: Response content
            
        Returns:
            Dict[str, Any]: Parsed strategy
        """
        try:
            # Extract JSON from content
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                return json.loads(json_match.group(0))
            return self._get_default_strategy('balanced')
        except Exception:
            return self._get_default_strategy('balanced')
    
    def _get_default_strategy(self, performance_mode: str) -> Dict[str, Any]:
        """Get default strategy
        
        Args:
            performance_mode: Performance mode
            
        Returns:
            Dict[str, Any]: Default strategy
        """
        base_strategy = {
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
            for key in base_strategy:
                if isinstance(base_strategy[key], dict) and 'strength' in base_strategy[key]:
                    base_strategy[key]['strength'] *= 0.3
            base_strategy['virtualization']['enabled'] = False
        elif performance_mode == 'security':
            for key in base_strategy:
                if isinstance(base_strategy[key], dict) and 'strength' in base_strategy[key]:
                    base_strategy[key]['strength'] *= 0.8
            base_strategy['virtualization']['enabled'] = True
        
        return base_strategy


# Register provider
AIProviderFactory.register_provider('anthropic', AnthropicProvider)
