"""热路径检测器"""

class HotpathDetector:
    """热路径检测器"""
    
    def __init__(self):
        """初始化热路径检测器"""
        pass
    
    def detect_hot_paths(self, cfg, ast_analyzer, code):
        """检测热路径
        
        Args:
            cfg: 控制流图
            ast_analyzer: AST分析器实例
            code: 源代码字符串
            
        Returns:
            list: 热路径列表
        """
        # 计算每个节点的权重
        node_weights = self._compute_node_weights(cfg, ast_analyzer, code)
        
        # 基于权重检测热路径
        hot_paths = self._find_hot_paths(cfg, node_weights)
        
        return hot_paths
    
    def _compute_node_weights(self, cfg, ast_analyzer, code):
        """计算每个节点的权重
        
        Args:
            cfg: 控制流图
            ast_analyzer: AST分析器实例
            code: 源代码字符串
            
        Returns:
            dict: 节点ID到权重的映射
        """
        node_weights = {}
        
        # 初始化所有节点的权重为1
        for node_id in cfg['nodes']:
            node_weights[node_id] = 1.0
        
        # 基于节点类型调整权重
        for node_id, node in cfg['nodes'].items():
            if node.type == 'entry' or node.type == 'exit':
                node_weights[node_id] = 0.0
            elif node.type == 'loop' or node.type == 'while_loop':
                # 循环节点权重更高
                node_weights[node_id] = 5.0
            elif node.type == 'if_condition':
                # 条件节点权重适中
                node_weights[node_id] = 2.0
            elif node.type == 'statement':
                # 基于语句类型调整权重
                if node.code:
                    if 'for' in node.code or 'while' in node.code:
                        node_weights[node_id] = 4.0
                    elif 'if' in node.code:
                        node_weights[node_id] = 2.0
                    elif 'return' in node.code:
                        node_weights[node_id] = 3.0
        
        # 基于节点的入度和出度调整权重
        for node_id, node in cfg['nodes'].items():
            # 入度越高，权重越高
            in_degree = len(node.predecessors)
            # 出度越高，权重越高
            out_degree = len(node.successors)
            
            # 调整权重
            node_weights[node_id] *= (1 + 0.2 * in_degree + 0.2 * out_degree)
        
        # 基于循环深度调整权重
        loop_depth = self._compute_loop_depth(cfg)
        for node_id in cfg['nodes']:
            if node_id in loop_depth:
                # 循环深度越深，权重越高
                node_weights[node_id] *= (1 + 0.5 * loop_depth[node_id])
        
        return node_weights
    
    def _compute_loop_depth(self, cfg):
        """计算每个节点的循环深度
        
        Args:
            cfg: 控制流图
            
        Returns:
            dict: 节点ID到循环深度的映射
        """
        loop_depth = {}
        
        # 初始化所有节点的循环深度为0
        for node_id in cfg['nodes']:
            loop_depth[node_id] = 0
        
        # 检测循环
        loops = self._detect_loops(cfg)
        
        # 计算每个节点的循环深度
        for loop in loops:
            for node_id in loop:
                loop_depth[node_id] += 1
        
        return loop_depth
    
    def _detect_loops(self, cfg):
        """检测控制流图中的循环
        
        Args:
            cfg: 控制流图
            
        Returns:
            list: 循环列表，每个循环是一个节点ID集合
        """
        loops = []
        
        # 使用深度优先搜索检测循环
        visited = set()
        path = []
        
        def dfs(node):
            if node.id in visited:
                # 检测到循环
                if node.id in path:
                    # 提取循环
                    loop_start = path.index(node.id)
                    loop = path[loop_start:]
                    loops.append(set(loop))
                return
            
            visited.add(node.id)
            path.append(node.id)
            
            for succ in node.successors:
                dfs(succ)
            
            path.pop()
        
        # 从入口节点开始DFS
        dfs(cfg['entry'])
        
        return loops
    
    def _find_hot_paths(self, cfg, node_weights):
        """基于节点权重找到热路径
        
        Args:
            cfg: 控制流图
            node_weights: 节点权重
            
        Returns:
            list: 热路径列表
        """
        hot_paths = []
        
        # 使用贪心算法找到权重最高的路径
        current_node = cfg['entry']
        path = [current_node.id]
        
        while current_node != cfg['exit']:
            # 选择权重最高的后继节点
            max_weight = -1
            next_node = None
            
            for succ in current_node.successors:
                if node_weights[succ.id] > max_weight:
                    max_weight = node_weights[succ.id]
                    next_node = succ
            
            if next_node is None:
                break
            
            path.append(next_node.id)
            current_node = next_node
        
        # 如果找到有效路径，添加到热路径列表
        if len(path) > 2:
            hot_paths.append(path)
        
        # 寻找其他可能的热路径
        # 这里可以实现更复杂的算法，如基于权重阈值的路径搜索
        
        return hot_paths
    
    def get_hot_path_info(self, hot_paths, cfg, ast_analyzer, code):
        """获取热路径的详细信息
        
        Args:
            hot_paths: 热路径列表
            cfg: 控制流图
            ast_analyzer: AST分析器实例
            code: 源代码字符串
            
        Returns:
            list: 热路径详细信息列表
        """
        hot_path_info = []
        
        for path in hot_paths:
            path_nodes = []
            path_weight = 0.0
            
            for node_id in path:
                node = cfg['nodes'][node_id]
                path_nodes.append({
                    'id': node_id,
                    'type': node.type,
                    'code': node.code,
                    'start_line': node.start_line,
                    'end_line': node.end_line
                })
                # 计算路径权重
                if node.type not in ['entry', 'exit']:
                    if node.type == 'loop' or node.type == 'while_loop':
                        path_weight += 5.0
                    elif node.type == 'if_condition':
                        path_weight += 2.0
                    else:
                        path_weight += 1.0
            
            hot_path_info.append({
                'path': path,
                'nodes': path_nodes,
                'weight': path_weight,
                'length': len(path)
            })
        
        return hot_path_info
