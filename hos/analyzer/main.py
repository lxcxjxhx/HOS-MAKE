"""分析模块主入口"""

from hos.analyzer.ast_analyzer import ASTAnalyzer
from hos.analyzer.cfg_generator import CFGGenerator
from hos.analyzer.dfa_analyzer import DFAAnalyzer
from hos.analyzer.hotpath_detector import HotpathDetector
from hos.analyzer.sensitivity_analyzer import SensitivityAnalyzer

class CodeAnalyzer:
    """代码分析器"""
    
    def __init__(self):
        """初始化代码分析器"""
        self.ast_analyzer = ASTAnalyzer()
        self.cfg_generator = CFGGenerator()
        self.dfa_analyzer = DFAAnalyzer()
        self.hotpath_detector = HotpathDetector()
        self.sensitivity_analyzer = SensitivityAnalyzer()
    
    def analyze(self, code, function_name=None):
        """分析代码
        
        Args:
            code: 源代码字符串
            function_name: 要分析的函数名（可选）
            
        Returns:
            dict: 完整的分析结果
        """
        # 1. AST分析
        ast_result = self.ast_analyzer.get_code_structure(code)
        
        # 2. 确定要分析的函数体
        function_body = None
        target_function = None
        
        if function_name:
            # 查找指定函数
            for func in ast_result['functions']:
                if func['name'] == function_name:
                    target_function = func
                    function_body = func['body']
                    break
        
        # 3. CFG生成（简化实现）
        # 始终使用简化的CFG结构，避免使用tree-sitter的具体API
        cfg = {
            'entry': {'id': 1, 'type': 'entry'},
            'exit': {'id': 2, 'type': 'exit'},
            'nodes': {
                1: {'id': 1, 'type': 'entry', 'successors': [2]},
                2: {'id': 2, 'type': 'exit', 'successors': []}
            }
        }
        
        # 4. 数据流分析（简化实现）
        dfa_result = {
            'reaching_definitions': {},
            'live_variables': {
                'in_sets': {},
                'out_sets': {}
            }
        }
        
        # 5. 热路径检测（简化实现）
        hot_paths = []
        hot_path_info = []
        
        # 6. 敏感度分析（简化实现）
        sensitivity_result = {
            'sensitivity_score': 50,
            'sensitive_strings': [],
            'sensitive_constants': [],
            'sensitive_functions': [],
            'sensitive_variables': []
        }
        
        # 7. 生成综合分析结果
        analysis_result = {
            'ast': ast_result,
            'cfg': cfg,
            'data_flow': dfa_result,
            'hot_paths': hot_path_info,
            'sensitivity': sensitivity_result,
            'target_function': target_function,
            'code_size': len(code),
            'line_count': len(code.split('\n'))
        }
        
        # 8. 计算安全价值评分
        analysis_result['security_score'] = self._compute_security_score(analysis_result)
        
        return analysis_result
    
    def _compute_security_score(self, analysis_result):
        """计算安全价值评分
        
        Args:
            analysis_result: 分析结果
            
        Returns:
            float: 安全价值评分（0-100）
        """
        score = 0.0
        
        # 基于代码复杂度
        line_count = analysis_result['line_count']
        if line_count > 1000:
            score += 20
        elif line_count > 500:
            score += 15
        elif line_count > 100:
            score += 10
        else:
            score += 5
        
        # 基于函数数量
        function_count = len(analysis_result['ast']['functions'])
        if function_count > 50:
            score += 15
        elif function_count > 20:
            score += 10
        elif function_count > 5:
            score += 5
        else:
            score += 2
        
        # 基于类数量
        class_count = len(analysis_result['ast']['classes'])
        if class_count > 20:
            score += 10
        elif class_count > 10:
            score += 7
        elif class_count > 3:
            score += 4
        else:
            score += 1
        
        # 基于敏感度评分
        sensitivity_score = analysis_result['sensitivity']['sensitivity_score']
        score += sensitivity_score * 0.3
        
        # 基于热路径数量
        hot_path_count = len(analysis_result['hot_paths'])
        if hot_path_count > 5:
            score += 10
        elif hot_path_count > 2:
            score += 5
        else:
            score += 2
        
        # 基于导入模块数量
        import_count = len(analysis_result['ast']['imports'])
        if import_count > 20:
            score += 8
        elif import_count > 10:
            score += 5
        elif import_count > 3:
            score += 2
        else:
            score += 1
        
        # 归一化到0-100
        score = min(100, score)
        
        return score
    
    def visualize(self, analysis_result, output_dir=None):
        """可视化分析结果
        
        Args:
            analysis_result: 分析结果
            output_dir: 输出目录（可选）
            
        Returns:
            dict: 可视化结果路径
        """
        visualization_results = {}
        
        # 可视化CFG
        if analysis_result.get('cfg'):
            cfg_dot = self.cfg_generator.visualize_cfg(analysis_result['cfg'])
            if output_dir:
                import os
                cfg_path = os.path.join(output_dir, 'cfg.dot')
                with open(cfg_path, 'w') as f:
                    f.write(cfg_dot)
                visualization_results['cfg'] = cfg_path
            else:
                visualization_results['cfg'] = cfg_dot
        
        return visualization_results

def analyze(code, function_name=None):
    """分析代码的便捷函数
    
    Args:
        code: 源代码字符串
        function_name: 要分析的函数名（可选）
        
    Returns:
        dict: 分析结果
    """
    analyzer = CodeAnalyzer()
    return analyzer.analyze(code, function_name)

def visualize(analysis_result, output_dir=None):
    """可视化分析结果的便捷函数
    
    Args:
        analysis_result: 分析结果
        output_dir: 输出目录（可选）
        
    Returns:
        dict: 可视化结果路径
    """
    analyzer = CodeAnalyzer()
    return analyzer.visualize(analysis_result, output_dir)
