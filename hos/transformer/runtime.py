"""运行时保护层模块"""

import random
import re
import os
import sys
import time

class RuntimeProtector:
    """运行时保护层"""
    
    def __init__(self):
        """初始化运行时保护层"""
        self.protect_counter = 0
    
    def transform(self, code, strategy):
        """应用运行时保护
        
        Args:
            code: 源代码字符串
            strategy: 混淆策略
            
        Returns:
            str: 变换后的代码
        """
        transformed_code = code
        
        # 应用调试器检测
        if strategy.runtime.get('debugger_detection', False):
            transformed_code = self._add_debugger_detection(transformed_code)
        
        # 应用内存完整性校验
        if strategy.runtime.get('memory_integrity', False):
            transformed_code = self._add_memory_integrity_check(transformed_code)
        
        # 应用时序检测
        if strategy.runtime.get('timing_detection', False):
            transformed_code = self._add_timing_detection(transformed_code)
        
        # 应用环境绑定
        if strategy.runtime.get('environment_binding', False):
            transformed_code = self._add_environment_binding(transformed_code)
        
        # 应用防篡改
        if strategy.runtime.get('anti_tampering', False):
            transformed_code = self._add_anti_tampering(transformed_code)
        
        return transformed_code
    
    def _add_debugger_detection(self, code):
        """添加调试器检测
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 生成调试器检测函数
        debugger_detection = self._generate_debugger_detection()
        
        # 添加到代码开头
        code = debugger_detection + '\n\n' + code
        
        # 在函数开头添加检测
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):\s*(.*?)(?=def|$)', re.DOTALL)
        
        def replace_function(match):
            function_name = match.group(1)
            params = match.group(2)
            body = match.group(3)
            
            # 添加检测调用
            indent = self._get_indent(body)
            detection_call = f"{indent}_check_debugger()\n"
            body = detection_call + body
            
            return f"def {function_name}({params}):\n{body}"
        
        return function_pattern.sub(replace_function, code)
    
    def _generate_debugger_detection(self):
        """生成调试器检测函数
        
        Returns:
            str: 调试器检测函数代码
        """
        detection_code = "def _check_debugger():\n"
        detection_code += "    import sys\n"
        detection_code += "    import os\n"
        detection_code += "    # 检测调试器\n"
        detection_code += "    # 方法1: 检查traceback模块\n"
        detection_code += "    try:\n"
        detection_code += "        import traceback\n"
        detection_code += "        # 检查调用栈深度\n"
        detection_code += "        if len(traceback.extract_stack()) > 10:\n"
        detection_code += "            raise RuntimeError('调试器检测到!')\n"
        detection_code += "    except:\n"
        detection_code += "        pass\n"
        detection_code += "    # 方法2: 检查进程名\n"
        detection_code += "    try:\n"
        detection_code += "        import psutil\n"
        detection_code += "        current_process = psutil.Process(os.getpid())\n"
        detection_code += "        # 检查是否有调试器附加\n"
        detection_code += "        for proc in psutil.process_iter(['name']):\n"
        detection_code += "            try:\n"
        detection_code += "                if 'debug' in proc.info['name'].lower():\n"
        detection_code += "                    raise RuntimeError('调试器检测到!')\n"
        detection_code += "            except:\n"
        detection_code += "                pass\n"
        detection_code += "    except ImportError:\n"
        detection_code += "        pass\n"
        detection_code += "    return True"
        
        return detection_code
    
    def _add_memory_integrity_check(self, code):
        """添加内存完整性校验
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 生成内存完整性校验函数
        integrity_check = self._generate_memory_integrity_check()
        
        # 添加到代码开头
        code = integrity_check + '\n\n' + code
        
        # 在函数开头添加检测
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):\s*(.*?)(?=def|$)', re.DOTALL)
        
        def replace_function(match):
            function_name = match.group(1)
            params = match.group(2)
            body = match.group(3)
            
            # 添加检测调用
            indent = self._get_indent(body)
            detection_call = f"{indent}_check_memory_integrity('{function_name}')\n"
            body = detection_call + body
            
            return f"def {function_name}({params}):\n{body}"
        
        return function_pattern.sub(replace_function, code)
    
    def _generate_memory_integrity_check(self):
        """生成内存完整性校验函数
        
        Returns:
            str: 内存完整性校验函数代码
        """
        check_code = "def _check_memory_integrity(function_name):\n"
        check_code += "    import hashlib\n"
        check_code += "    import inspect\n"
        check_code += "    # 计算函数代码的哈希值\n"
        check_code += "    try:\n"
        check_code += "        # 获取调用者的代码\n"
        check_code += "        caller_frame = inspect.currentframe().f_back\n"
        check_code += "        caller_code = inspect.getsource(caller_frame)\n"
        check_code += "        # 计算哈希值\n"
        check_code += "        expected_hash = hashlib.md5(caller_code.encode()).hexdigest()\n"
        check_code += "        # 这里应该存储预期的哈希值\n"
        check_code += "        # 简化版：只检查代码是否被修改\n"
        check_code += "        if len(caller_code) < 10:\n"
        check_code += "            raise RuntimeError('代码被篡改!')\n"
        check_code += "    except:\n"
        check_code += "        pass\n"
        check_code += "    return True"
        
        return check_code
    
    def _add_timing_detection(self, code):
        """添加时序检测
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 生成时序检测函数
        timing_detection = self._generate_timing_detection()
        
        # 添加到代码开头
        code = timing_detection + '\n\n' + code
        
        # 在函数开头和结尾添加检测
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):\s*(.*?)(?=def|$)', re.DOTALL)
        
        def replace_function(match):
            function_name = match.group(1)
            params = match.group(2)
            body = match.group(3)
            
            # 添加检测调用
            indent = self._get_indent(body)
            start_call = f"{indent}_start_timing()\n"
            
            # 在函数结尾添加结束检测
            lines = body.strip().split('\n')
            if lines:
                # 找到return语句
                for i in range(len(lines)-1, -1, -1):
                    if 'return' in lines[i]:
                        lines[i] = f"{indent}_check_timing()\n{lines[i]}"
                        break
                else:
                    # 如果没有return语句，在最后添加
                    lines.append(f"{indent}_check_timing()")
                body = '\n'.join(lines)
            
            body = start_call + body
            
            return f"def {function_name}({params}):\n{body}"
        
        return function_pattern.sub(replace_function, code)
    
    def _generate_timing_detection(self):
        """生成时序检测函数
        
        Returns:
            str: 时序检测函数代码
        """
        timing_code = "_start_time = 0\n"
        timing_code += "def _start_timing():\n"
        timing_code += "    global _start_time\n"
        timing_code += "    import time\n"
        timing_code += "    _start_time = time.time()\n"
        timing_code += "\n"
        timing_code += "def _check_timing():\n"
        timing_code += "    global _start_time\n"
        timing_code += "    import time\n"
        timing_code += "    current_time = time.time()\n"
        timing_code += "    elapsed = current_time - _start_time\n"
        timing_code += "    # 检查执行时间是否过长（可能被单步调试）\n"
        timing_code += "    if elapsed > 10.0:\n"
        timing_code += "        raise RuntimeError('执行时间过长，可能被调试!')\n"
        timing_code += "    return True"
        
        return timing_code
    
    def _add_environment_binding(self, code):
        """添加环境绑定
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 生成环境绑定函数
        env_binding = self._generate_environment_binding()
        
        # 添加到代码开头
        code = env_binding + '\n\n' + code
        
        # 在函数开头添加检测
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):\s*(.*?)(?=def|$)', re.DOTALL)
        
        def replace_function(match):
            function_name = match.group(1)
            params = match.group(2)
            body = match.group(3)
            
            # 添加检测调用
            indent = self._get_indent(body)
            binding_call = f"{indent}_check_environment()\n"
            body = binding_call + body
            
            return f"def {function_name}({params}):\n{body}"
        
        return function_pattern.sub(replace_function, code)
    
    def _generate_environment_binding(self):
        """生成环境绑定函数
        
        Returns:
            str: 环境绑定函数代码
        """
        binding_code = "def _check_environment():\n"
        binding_code += "    import os\n"
        binding_code += "    import platform\n"
        binding_code += "    # 收集环境信息\n"
        binding_code += "    env_info = {}\n"
        binding_code += "    env_info['os'] = platform.system()\n"
        binding_code += "    env_info['machine'] = platform.machine()\n"
        binding_code += "    env_info['python_version'] = platform.python_version()\n"
        binding_code += "    # 这里应该与预存储的环境信息比较\n"
        binding_code += "    # 简化版：只检查基本环境\n"
        binding_code += "    # 实际实现中，应该存储环境指纹并进行比较\n"
        binding_code += "    return True"
        
        return binding_code
    
    def _add_anti_tampering(self, code):
        """添加防篡改
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 生成防篡改函数
        anti_tampering = self._generate_anti_tampering()
        
        # 添加到代码开头
        code = anti_tampering + '\n\n' + code
        
        # 在函数开头添加检测
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):\s*(.*?)(?=def|$)', re.DOTALL)
        
        def replace_function(match):
            function_name = match.group(1)
            params = match.group(2)
            body = match.group(3)
            
            # 添加检测调用
            indent = self._get_indent(body)
            tampering_call = f"{indent}_check_tampering()\n"
            body = tampering_call + body
            
            return f"def {function_name}({params}):\n{body}"
        
        return function_pattern.sub(replace_function, code)
    
    def _generate_anti_tampering(self):
        """生成防篡改函数
        
        Returns:
            str: 防篡改函数代码
        """
        tampering_code = "def _check_tampering():\n"
        tampering_code += "    import hashlib\n"
        tampering_code += "    import os\n"
        tampering_code += "    # 检查文件完整性\n"
        tampering_code += "    try:\n"
        tampering_code += "        # 获取当前文件路径\n"
        tampering_code += "        import inspect\n"
        tampering_code += "        current_file = inspect.getfile(inspect.currentframe())\n"
        tampering_code += "        # 计算文件哈希值\n"
        tampering_code += "        with open(current_file, 'rb') as f:\n"
        tampering_code += "            file_hash = hashlib.md5(f.read()).hexdigest()\n"
        tampering_code += "        # 这里应该存储预期的哈希值\n"
        tampering_code += "        # 简化版：只检查文件是否存在\n"
        tampering_code += "        if not os.path.exists(current_file):\n"
        tampering_code += "            raise RuntimeError('文件不存在!')\n"
        tampering_code += "    except:\n"
        tampering_code += "        pass\n"
        tampering_code += "    return True"
        
        return tampering_code
    
    def _get_indent(self, code):
        """获取代码的缩进
        
        Args:
            code: 代码字符串
            
        Returns:
            str: 缩进字符串
        """
        lines = code.strip().split('\n')
        if not lines:
            return ''
        
        first_line = lines[0]
        indent = ''
        for char in first_line:
            if char in (' ', '\t'):
                indent += char
            else:
                break
        
        return indent
