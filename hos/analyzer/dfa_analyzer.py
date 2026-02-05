"""数据流分析（DFA）模块"""

class DFAAnalyzer:
    """数据流分析器"""
    
    def __init__(self):
        """初始化DFA分析器"""
        pass
    
    def analyze_reaching_definitions(self, cfg):
        """到达定义分析
        
        Args:
            cfg: 控制流图
            
        Returns:
            dict: 每个节点的到达定义集合
        """
        # 初始化IN和OUT集合
        in_sets = {}
        out_sets = {}
        
        # 初始化所有节点的IN和OUT集合为空
        for node_id in cfg['nodes']:
            in_sets[node_id] = set()
            out_sets[node_id] = set()
        
        # 迭代求解直到收敛
        changed = True
        while changed:
            changed = False
            
            # 按照节点顺序处理
            for node_id, node in cfg['nodes'].items():
                # 跳过入口和出口节点
                if node.type in ['entry', 'exit']:
                    continue
                
                # 计算IN[node] = 所有前驱节点的OUT集合的并集
                new_in = set()
                for pred in node.predecessors:
                    new_in.update(out_sets[pred.id])
                
                # 计算OUT[node] = IN[node] - KILL[node] ∪ GEN[node]
                kill = self._compute_kill_set(node)
                gen = self._compute_gen_set(node)
                new_out = (new_in - kill) | gen
                
                # 检查是否有变化
                if new_in != in_sets[node_id] or new_out != out_sets[node_id]:
                    in_sets[node_id] = new_in
                    out_sets[node_id] = new_out
                    changed = True
        
        return {
            'in_sets': in_sets,
            'out_sets': out_sets
        }
    
    def analyze_live_variables(self, cfg):
        """活跃变量分析
        
        Args:
            cfg: 控制流图
            
        Returns:
            dict: 每个节点的活跃变量集合
        """
        # 初始化IN和OUT集合
        in_sets = {}
        out_sets = {}
        
        # 初始化所有节点的IN和OUT集合为空
        for node_id in cfg['nodes']:
            in_sets[node_id] = set()
            out_sets[node_id] = set()
        
        # 迭代求解直到收敛
        changed = True
        while changed:
            changed = False
            
            # 按照逆序处理节点
            for node_id, node in reversed(list(cfg['nodes'].items())):
                # 跳过入口和出口节点
                if node.type in ['entry', 'exit']:
                    continue
                
                # 计算OUT[node] = 所有后继节点的IN集合的并集
                new_out = set()
                for succ in node.successors:
                    new_out.update(in_sets[succ.id])
                
                # 计算IN[node] = (OUT[node] - KILL[node]) ∪ GEN[node]
                kill = self._compute_live_kill_set(node)
                gen = self._compute_live_gen_set(node)
                new_in = (new_out - kill) | gen
                
                # 检查是否有变化
                if new_in != in_sets[node_id] or new_out != out_sets[node_id]:
                    in_sets[node_id] = new_in
                    out_sets[node_id] = new_out
                    changed = True
        
        return {
            'in_sets': in_sets,
            'out_sets': out_sets
        }
    
    def _compute_kill_set(self, node):
        """计算KILL集合（到达定义）
        
        Args:
            node: CFG节点
            
        Returns:
            set: KILL集合
        """
        kill = set()
        
        # 简单实现：假设节点代码中定义的变量会杀死所有之前的定义
        if node.code:
            # 这里需要根据实际的代码分析来提取变量定义
            # 简化版：通过正则表达式匹配变量定义
            import re
            # 匹配简单的变量赋值
            matches = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=', node.code)
            for var in matches:
                kill.add(var)
        
        return kill
    
    def _compute_gen_set(self, node):
        """计算GEN集合（到达定义）
        
        Args:
            node: CFG节点
            
        Returns:
            set: GEN集合
        """
        gen = set()
        
        # 简单实现：提取节点代码中定义的变量
        if node.code:
            import re
            # 匹配简单的变量赋值
            matches = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=', node.code)
            for var in matches:
                gen.add(var)
        
        return gen
    
    def _compute_live_kill_set(self, node):
        """计算KILL集合（活跃变量）
        
        Args:
            node: CFG节点
            
        Returns:
            set: KILL集合
        """
        kill = set()
        
        # 简单实现：假设节点代码中定义的变量会杀死该变量
        if node.code:
            import re
            # 匹配简单的变量赋值
            matches = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=', node.code)
            for var in matches:
                kill.add(var)
        
        return kill
    
    def _compute_live_gen_set(self, node):
        """计算GEN集合（活跃变量）
        
        Args:
            node: CFG节点
            
        Returns:
            set: GEN集合
        """
        gen = set()
        
        # 简单实现：提取节点代码中使用的变量（除了定义的变量）
        if node.code:
            import re
            # 匹配所有变量引用
            all_vars = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', node.code))
            # 匹配定义的变量
            defined_vars = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=', node.code))
            # 使用的变量 = 所有变量 - 定义的变量
            used_vars = all_vars - defined_vars
            
            # 过滤掉关键字
            keywords = {'if', 'else', 'for', 'while', 'try', 'except', 'finally', 'return', 'def', 'class'}
            gen = used_vars - keywords
        
        return gen
    
    def analyze_constant_propagation(self, cfg):
        """常量传播分析
        
        Args:
            cfg: 控制流图
            
        Returns:
            dict: 每个节点的常量传播信息
        """
        # 初始化IN和OUT集合
        in_sets = {}
        out_sets = {}
        
        # 初始化所有节点的IN和OUT集合为top（空字典）
        for node_id in cfg['nodes']:
            in_sets[node_id] = {}
            out_sets[node_id] = {}
        
        # 迭代求解直到收敛
        changed = True
        while changed:
            changed = False
            
            # 按照节点顺序处理
            for node_id, node in cfg['nodes'].items():
                # 跳过入口和出口节点
                if node.type in ['entry', 'exit']:
                    continue
                
                # 计算IN[node] = 所有前驱节点的OUT集合的交集
                new_in = None
                for pred in node.predecessors:
                    if new_in is None:
                        new_in = out_sets[pred.id].copy()
                    else:
                        # 计算交集：只保留两个集合中都存在且值相同的变量
                        common_vars = set(new_in.keys()) & set(out_sets[pred.id].keys())
                        temp_in = {}
                        for var in common_vars:
                            if new_in[var] == out_sets[pred.id][var]:
                                temp_in[var] = new_in[var]
                        new_in = temp_in
                
                if new_in is None:
                    new_in = {}
                
                # 计算OUT[node] = transfer(IN[node])
                new_out = self._transfer_constant_propagation(new_in, node)
                
                # 检查是否有变化
                if new_in != in_sets[node_id] or new_out != out_sets[node_id]:
                    in_sets[node_id] = new_in
                    out_sets[node_id] = new_out
                    changed = True
        
        return {
            'in_sets': in_sets,
            'out_sets': out_sets
        }
    
    def _transfer_constant_propagation(self, in_set, node):
        """常量传播的transfer函数
        
        Args:
            in_set: 输入的常量集合
            node: CFG节点
            
        Returns:
            dict: 输出的常量集合
        """
        out_set = in_set.copy()
        
        if node.code:
            import re
            # 匹配简单的变量赋值，如 x = 10 或 x = y + z
            matches = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)', node.code)
            for var, expr in matches:
                # 尝试计算表达式的值
                try:
                    # 替换变量为常量值
                    eval_expr = expr
                    for v, val in out_set.items():
                        eval_expr = eval_expr.replace(v, str(val))
                    # 计算表达式
                    value = eval(eval_expr)
                    # 更新out_set
                    out_set[var] = value
                except:
                    # 如果表达式无法计算为常量，移除该变量
                    if var in out_set:
                        del out_set[var]
        
        return out_set
    
    def get_data_flow_info(self, cfg):
        """获取完整的数据流信息
        
        Args:
            cfg: 控制流图
            
        Returns:
            dict: 完整的数据流分析结果
        """
        reaching_defs = self.analyze_reaching_definitions(cfg)
        live_vars = self.analyze_live_variables(cfg)
        constant_propagation = self.analyze_constant_propagation(cfg)
        
        return {
            'reaching_definitions': reaching_defs,
            'live_variables': live_vars,
            'constant_propagation': constant_propagation
        }
