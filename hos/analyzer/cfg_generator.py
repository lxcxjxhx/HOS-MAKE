"""控制流图（CFG）生成器"""

class CFGNode:
    """CFG节点"""
    
    def __init__(self, id, type, code=None, start_line=None, end_line=None):
        """初始化CFG节点
        
        Args:
            id: 节点ID
            type: 节点类型（如'block', 'if', 'loop'等）
            code: 节点对应的代码
            start_line: 起始行号
            end_line: 结束行号
        """
        self.id = id
        self.type = type
        self.code = code
        self.start_line = start_line
        self.end_line = end_line
        self.successors = []  # 后继节点
        self.predecessors = []  # 前驱节点
    
    def add_successor(self, node):
        """添加后继节点
        
        Args:
            node: 后继节点
        """
        if node not in self.successors:
            self.successors.append(node)
            node.predecessors.append(self)
    
    def __repr__(self):
        return f"CFGNode({self.id}, {self.type}, {self.start_line}-{self.end_line})"

class CFGGenerator:
    """CFG生成器"""
    
    def __init__(self):
        """初始化CFG生成器"""
        self.node_counter = 0
    
    def generate_node_id(self):
        """生成唯一节点ID
        
        Returns:
            int: 节点ID
        """
        self.node_counter += 1
        return self.node_counter
    
    def generate_cfg(self, ast_analyzer, code, function_body=None):
        """生成控制流图
        
        Args:
            ast_analyzer: AST分析器实例
            code: 源代码字符串
            function_body: 函数体节点（可选）
            
        Returns:
            dict: CFG分析结果，包含入口节点和所有节点
        """
        # 重置节点计数器
        self.node_counter = 0
        
        # 如果没有指定函数体，分析整个代码
        if function_body is None:
            tree = ast_analyzer.parse(code)
            root_node = ast_analyzer.get_root_node(tree)
            function_body = root_node
        
        # 生成CFG
        entry_node = CFGNode(self.generate_node_id(), 'entry')
        nodes = {entry_node.id: entry_node}
        
        # 从入口节点开始构建CFG
        current_node = entry_node
        
        # 分析函数体
        current_node = self._process_block(function_body, current_node, nodes, ast_analyzer, code)
        
        # 创建出口节点
        exit_node = CFGNode(self.generate_node_id(), 'exit')
        current_node.add_successor(exit_node)
        nodes[exit_node.id] = exit_node
        
        return {
            'entry': entry_node,
            'exit': exit_node,
            'nodes': nodes
        }
    
    def _process_block(self, block_node, current_node, nodes, ast_analyzer, code):
        """处理代码块
        
        Args:
            block_node: 代码块节点
            current_node: 当前节点
            nodes: 节点字典
            ast_analyzer: AST分析器实例
            code: 源代码字符串
            
        Returns:
            CFGNode: 处理完代码块后的当前节点
        """
        for child in block_node.children:
            if child.type == 'expression_statement':
                # 处理表达式语句
                stmt_node = CFGNode(
                    self.generate_node_id(),
                    'statement',
                    ast_analyzer.get_node_text(child, code),
                    child.start_point[0] + 1,
                    child.end_point[0] + 1
                )
                nodes[stmt_node.id] = stmt_node
                current_node.add_successor(stmt_node)
                current_node = stmt_node
            
            elif child.type == 'if_statement':
                # 处理if语句
                current_node = self._process_if_statement(child, current_node, nodes, ast_analyzer, code)
            
            elif child.type == 'for_statement':
                # 处理for循环
                current_node = self._process_for_statement(child, current_node, nodes, ast_analyzer, code)
            
            elif child.type == 'while_statement':
                # 处理while循环
                current_node = self._process_while_statement(child, current_node, nodes, ast_analyzer, code)
            
            elif child.type == 'try_statement':
                # 处理try语句
                current_node = self._process_try_statement(child, current_node, nodes, ast_analyzer, code)
            
            elif child.type == 'return_statement':
                # 处理return语句
                return_node = CFGNode(
                    self.generate_node_id(),
                    'return',
                    ast_analyzer.get_node_text(child, code),
                    child.start_point[0] + 1,
                    child.end_point[0] + 1
                )
                nodes[return_node.id] = return_node
                current_node.add_successor(return_node)
                current_node = return_node
            
            elif child.type == 'block':
                # 处理嵌套代码块
                current_node = self._process_block(child, current_node, nodes, ast_analyzer, code)
        
        return current_node
    
    def _process_if_statement(self, if_node, current_node, nodes, ast_analyzer, code):
        """处理if语句
        
        Args:
            if_node: if语句节点
            current_node: 当前节点
            nodes: 节点字典
            ast_analyzer: AST分析器实例
            code: 源代码字符串
            
        Returns:
            CFGNode: 处理完if语句后的当前节点
        """
        # 创建if条件节点
        condition_node = CFGNode(
            self.generate_node_id(),
            'if_condition',
            ast_analyzer.get_node_text(if_node, code),
            if_node.start_point[0] + 1,
            if_node.end_point[0] + 1
        )
        nodes[condition_node.id] = condition_node
        current_node.add_successor(condition_node)
        
        # 处理if分支
        if_body = None
        else_body = None
        
        for child in if_node.children:
            if child.type == 'block':
                if_body = child
            elif child.type == 'else_clause':
                for else_child in child.children:
                    if else_child.type == 'block':
                        else_body = else_child
        
        # 处理if分支
        if if_body:
            if_exit = self._process_block(if_body, condition_node, nodes, ast_analyzer, code)
        else:
            if_exit = condition_node
        
        # 处理else分支
        if else_body:
            else_exit = self._process_block(else_body, condition_node, nodes, ast_analyzer, code)
        else:
            else_exit = condition_node
        
        # 创建合并节点
        merge_node = CFGNode(self.generate_node_id(), 'merge')
        nodes[merge_node.id] = merge_node
        
        if if_exit != condition_node:
            if_exit.add_successor(merge_node)
        if else_exit != condition_node:
            else_exit.add_successor(merge_node)
        
        # 如果没有else分支，condition_node也需要指向merge_node
        if not else_body:
            condition_node.add_successor(merge_node)
        
        return merge_node
    
    def _process_for_statement(self, for_node, current_node, nodes, ast_analyzer, code):
        """处理for循环
        
        Args:
            for_node: for循环节点
            current_node: 当前节点
            nodes: 节点字典
            ast_analyzer: AST分析器实例
            code: 源代码字符串
            
        Returns:
            CFGNode: 处理完for循环后的当前节点
        """
        # 创建循环节点
        loop_node = CFGNode(
            self.generate_node_id(),
            'loop',
            ast_analyzer.get_node_text(for_node, code),
            for_node.start_point[0] + 1,
            for_node.end_point[0] + 1
        )
        nodes[loop_node.id] = loop_node
        current_node.add_successor(loop_node)
        
        # 处理循环体
        loop_body = None
        for child in for_node.children:
            if child.type == 'block':
                loop_body = child
                break
        
        if loop_body:
            body_exit = self._process_block(loop_body, loop_node, nodes, ast_analyzer, code)
            # 循环回到loop_node
            body_exit.add_successor(loop_node)
        
        # 创建循环出口节点
        loop_exit = CFGNode(self.generate_node_id(), 'loop_exit')
        nodes[loop_exit.id] = loop_exit
        
        # 从loop_node到exit的边（循环结束）
        loop_node.add_successor(loop_exit)
        
        return loop_exit
    
    def _process_while_statement(self, while_node, current_node, nodes, ast_analyzer, code):
        """处理while循环
        
        Args:
            while_node: while循环节点
            current_node: 当前节点
            nodes: 节点字典
            ast_analyzer: AST分析器实例
            code: 源代码字符串
            
        Returns:
            CFGNode: 处理完while循环后的当前节点
        """
        # 创建循环条件节点
        loop_node = CFGNode(
            self.generate_node_id(),
            'while_loop',
            ast_analyzer.get_node_text(while_node, code),
            while_node.start_point[0] + 1,
            while_node.end_point[0] + 1
        )
        nodes[loop_node.id] = loop_node
        current_node.add_successor(loop_node)
        
        # 处理循环体
        loop_body = None
        for child in while_node.children:
            if child.type == 'block':
                loop_body = child
                break
        
        if loop_body:
            body_exit = self._process_block(loop_body, loop_node, nodes, ast_analyzer, code)
            # 循环回到loop_node
            body_exit.add_successor(loop_node)
        
        # 创建循环出口节点
        loop_exit = CFGNode(self.generate_node_id(), 'loop_exit')
        nodes[loop_exit.id] = loop_exit
        
        # 从loop_node到exit的边（循环结束）
        loop_node.add_successor(loop_exit)
        
        return loop_exit
    
    def _process_try_statement(self, try_node, current_node, nodes, ast_analyzer, code):
        """处理try语句
        
        Args:
            try_node: try语句节点
            current_node: 当前节点
            nodes: 节点字典
            ast_analyzer: AST分析器实例
            code: 源代码字符串
            
        Returns:
            CFGNode: 处理完try语句后的当前节点
        """
        # 创建try节点
        try_block_node = CFGNode(
            self.generate_node_id(),
            'try_block',
            ast_analyzer.get_node_text(try_node, code),
            try_node.start_point[0] + 1,
            try_node.end_point[0] + 1
        )
        nodes[try_block_node.id] = try_block_node
        current_node.add_successor(try_block_node)
        
        # 处理try块
        try_body = None
        except_bodies = []
        finally_body = None
        
        for child in try_node.children:
            if child.type == 'block':
                if try_body is None:
                    try_body = child
                else:
                    except_bodies.append(child)
            elif child.type == 'finally_clause':
                for finally_child in child.children:
                    if finally_child.type == 'block':
                        finally_body = finally_child
        
        # 处理try块
        if try_body:
            try_exit = self._process_block(try_body, try_block_node, nodes, ast_analyzer, code)
        else:
            try_exit = try_block_node
        
        # 处理except块
        except_exits = []
        for i, except_body in enumerate(except_bodies):
            except_node = CFGNode(
                self.generate_node_id(),
                f'except_block_{i}',
                ast_analyzer.get_node_text(except_body, code),
                except_body.start_point[0] + 1,
                except_body.end_point[0] + 1
            )
            nodes[except_node.id] = except_node
            try_block_node.add_successor(except_node)
            
            except_exit = self._process_block(except_body, except_node, nodes, ast_analyzer, code)
            except_exits.append(except_exit)
        
        # 处理finally块
        if finally_body:
            finally_node = CFGNode(
                self.generate_node_id(),
                'finally_block',
                ast_analyzer.get_node_text(finally_body, code),
                finally_body.start_point[0] + 1,
                finally_body.end_point[0] + 1
            )
            nodes[finally_node.id] = finally_node
            
            # 所有路径都要经过finally
            if try_exit != try_block_node:
                try_exit.add_successor(finally_node)
            else:
                try_block_node.add_successor(finally_node)
            
            for except_exit in except_exits:
                except_exit.add_successor(finally_node)
            
            finally_exit = self._process_block(finally_body, finally_node, nodes, ast_analyzer, code)
            return finally_exit
        else:
            # 没有finally，创建合并节点
            merge_node = CFGNode(self.generate_node_id(), 'merge')
            nodes[merge_node.id] = merge_node
            
            if try_exit != try_block_node:
                try_exit.add_successor(merge_node)
            else:
                try_block_node.add_successor(merge_node)
            
            for except_exit in except_exits:
                except_exit.add_successor(merge_node)
            
            return merge_node
    
    def visualize_cfg(self, cfg, output_file=None):
        """可视化CFG
        
        Args:
            cfg: CFG分析结果
            output_file: 输出文件路径（可选）
            
        Returns:
            str: DOT格式的CFG
        """
        dot_content = "digraph CFG {\n"
        dot_content += "    node [shape=box];\n"
        
        # 添加节点
        for node_id, node in cfg['nodes'].items():
            label = f"{node.type}"
            if node.code:
                label += f"\\n{node.code[:50]}{'...' if len(node.code) > 50 else ''}"
            if node.start_line and node.end_line:
                label += f"\\n{node.start_line}-{node.end_line}"
            dot_content += f"    {node_id} [label=\"{label}\"];\n"
        
        # 添加边
        for node_id, node in cfg['nodes'].items():
            for successor in node.successors:
                dot_content += f"    {node_id} -> {successor.id};\n"
        
        dot_content += "}"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(dot_content)
        
        return dot_content
