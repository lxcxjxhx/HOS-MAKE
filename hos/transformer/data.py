"""数据变换模块"""

import random
import re
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class DataTransformer:
    """数据变换"""
    
    def __init__(self):
        """初始化数据变换器"""
        self.const_counter = 0
        self.string_counter = 0
        self.cache = {}
        self.string_cache = {}
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
        self.string_cache.clear()
    
    def transform(self, code, strategy):
        """应用数据变换
        
        Args:
            code: 源代码字符串
            strategy: 混淆策略
            
        Returns:
            str: 变换后的代码
        """
        transformed_code = code
        
        # 应用常量拆分
        if strategy.data.get('constant_splitting', False):
            transformed_code = self._split_constants(transformed_code)
        
        # 应用动态计算
        if strategy.data.get('dynamic_calculation', False):
            transformed_code = self._dynamic_calculation(transformed_code)
        
        # 应用编码表
        if strategy.data.get('encoding_table', False):
            transformed_code = self._add_encoding_table(transformed_code)
        
        # 应用多态编码
        if strategy.data.get('polymorphic_encoding', False):
            transformed_code = self._add_polymorphic_encoding(transformed_code)
        
        # 应用字符串加密
        if strategy.data.get('string_encryption', False):
            transformed_code = self._encrypt_strings(transformed_code)
        
        return transformed_code
    
    def _split_constants(self, code):
        """拆分常量
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 寻找数字常量
        number_pattern = re.compile(r'\b(\d+)\b')
        
        def replace_number(match):
            number = int(match.group(1))
            
            # 只处理较大的数字
            if number < 100:
                return match.group(1)
            
            # 拆分数字
            parts = self._split_number(number)
            
            # 生成拆分后的表达式
            var_name = f"_const_{random.randint(1000, 9999)}"
            expr = ' + '.join(map(str, parts))
            
            # 添加到代码开头
            nonlocal code
            code = f"{var_name} = {expr}\n{code}"
            
            return var_name
        
        return number_pattern.sub(replace_number, code)
    
    def _split_number(self, number):
        """拆分数字
        
        Args:
            number: 要拆分的数字
            
        Returns:
            list: 数字部分列表
        """
        parts = []
        remaining = number
        
        # 生成随机部分
        while remaining > 0:
            if remaining < 10:
                parts.append(remaining)
                break
            
            part = random.randint(1, remaining // 2)
            parts.append(part)
            remaining -= part
        
        # 确保至少有两个部分
        if len(parts) < 2:
            parts = [parts[0] // 2, parts[0] - parts[0] // 2]
        
        return parts
    
    def _dynamic_calculation(self, code):
        """动态计算
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 寻找赋值语句
        assign_pattern = re.compile(r'(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(\d+)')
        
        def replace_assign(match):
            indent = match.group(1)
            var_name = match.group(2)
            value = int(match.group(3))
            
            # 生成动态计算表达式
            expr = self._generate_dynamic_expr(value)
            
            return f"{indent}{var_name} = {expr}"
        
        return assign_pattern.sub(replace_assign, code)
    
    def _generate_dynamic_expr(self, value):
        """生成动态计算表达式
        
        Args:
            value: 原始值
            
        Returns:
            str: 动态计算表达式
        """
        if value <= 1:
            return str(value)
        
        # 检查缓存
        if value in self.cache:
            return self.cache[value]
        
        # 高级动态计算技术
        techniques = [
            self._generate_polynomial_expr,
            self._generate_trigonometric_expr,
            self._generate_bitwise_expr,
            self._generate_complex_arithmetic_expr
        ]
        
        # 随机选择一种技术
        technique = random.choice(techniques)
        expr = technique(value)
        
        # 缓存结果
        self.cache[value] = expr
        
        return expr
    
    def _generate_polynomial_expr(self, value):
        """生成多项式表达式
        
        Args:
            value: 原始值
            
        Returns:
            str: 多项式表达式
        """
        # 生成形如 (a * x + b) * c - d 的表达式
        a = random.randint(2, 5)
        c = random.randint(2, 5)
        b = random.randint(1, 10)
        d = (a * c * random.randint(1, value // (a * c))) + b * c
        
        x = (value + d - b * c) // (a * c)
        return f"({a} * {x} + {b}) * {c} - {d}"
    
    def _generate_trigonometric_expr(self, value):
        """生成三角函数表达式
        
        Args:
            value: 原始值
            
        Returns:
            str: 三角函数表达式
        """
        # 生成形如 int(abs(sin(a)) * b) 的表达式
        a = random.randint(100, 1000)
        b = value * random.randint(10, 100)
        return f"int(abs(__import__('math').sin({a})) * {b})"
    
    def _generate_bitwise_expr(self, value):
        """生成位运算表达式
        
        Args:
            value: 原始值
            
        Returns:
            str: 位运算表达式
        """
        # 生成形如 (a ^ b) & c 的表达式
        a = random.randint(value, value * 2)
        b = a ^ value
        c = (1 << (value.bit_length() + 1)) - 1
        return f"({a} ^ {b}) & {c}"
    
    def _generate_complex_arithmetic_expr(self, value):
        """生成复杂算术表达式
        
        Args:
            value: 原始值
            
        Returns:
            str: 复杂算术表达式
        """
        operations = ['+', '-', '*', '//', '%']
        expr_parts = []
        
        # 生成第一个操作数
        max_first_op = max(1, value // 2)
        first_op = random.randint(1, max_first_op)
        expr_parts.append(str(first_op))
        
        remaining = value - first_op
        
        # 生成后续操作
        while remaining != 0:
            op = random.choice(operations)
            if op == '+':
                next_op = random.randint(1, remaining)
                expr_parts.append('+')
                expr_parts.append(str(next_op))
                remaining -= next_op
            elif op == '-':
                # 确保结果不会为负
                next_op = random.randint(1, value // 2)
                expr_parts.append('-')
                expr_parts.append(str(next_op))
                expr_parts.append('+')
                expr_parts.append(str(next_op + remaining))
                remaining = 0
            elif op == '*':
                # 寻找因子
                factors = []
                for i in range(2, value // 2 + 1):
                    if value % i == 0:
                        factors.append(i)
                
                if factors:
                    factor = random.choice(factors)
                    expr_parts.append('*')
                    expr_parts.append(str(factor))
                    expr_parts.append('*')
                    expr_parts.append(str(value // factor))
                    remaining = 0
                else:
                    # 如果没有因子，使用加法
                    expr_parts.append('+')
                    expr_parts.append(str(remaining))
                    remaining = 0
            elif op == '//' or op == '%':
                # 生成整除或取模表达式
                divisor = random.randint(2, 10)
                quotient = value // divisor
                remainder = value % divisor
                if op == '//':
                    expr_parts.append('*')
                    expr_parts.append(str(divisor))
                    expr_parts.append('//')
                    expr_parts.append(str(divisor))
                else:
                    expr_parts.append('*')
                    expr_parts.append(str(divisor))
                    expr_parts.append('%')
                    expr_parts.append(str(divisor))
                    expr_parts.append('+')
                    expr_parts.append(str(remainder))
                remaining = 0
        
        return ' '.join(expr_parts)
    
    def _add_polymorphic_encoding(self, code):
        """添加多态编码
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 生成多态编码函数
        encode_func = f"_encode_{random.randint(1000, 9999)}"
        decode_func = f"_decode_{random.randint(1000, 9999)}"
        
        # 生成随机编码表
        encode_table = {}
        decode_table = {}
        for i in range(256):
            encoded = random.randint(0, 255)
            encode_table[i] = encoded
            decode_table[encoded] = i
        
        # 添加编码函数
        encode_code = f"""
{encode_func} = {encode_table}

{decode_func} = {decode_table}

"""
        
        return encode_code + code
    
    def _add_encoding_table(self, code):
        """添加编码表
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 生成编码表
        encoding_table = self._generate_encoding_table()
        decode_function = self._generate_decode_function()
        
        # 添加到代码开头
        encoded_code = f"{encoding_table}\n{decode_function}\n{code}"
        
        return encoded_code
    
    def _generate_encoding_table(self):
        """生成编码表
        
        Returns:
            str: 编码表代码
        """
        table_name = f"_encoding_table_{random.randint(1000, 9999)}"
        
        # 生成随机编码表
        table = {}
        for i in range(256):
            table[i] = random.randint(0, 255)
        
        # 生成编码表代码
        table_code = f"{table_name} = " + str(table)
        
        return table_code
    
    def _generate_decode_function(self):
        """生成解码函数
        
        Returns:
            str: 解码函数代码
        """
        func_name = f"_decode_{random.randint(1000, 9999)}"
        table_name = f"_encoding_table_{random.randint(1000, 9999)}"
        
        # 生成解码函数
        func_code = f"def {func_name}(data):\n"
        func_code += f"    result = ''\n"
        func_code += f"    for c in data:\n"
        func_code += f"        result += chr({table_name}[ord(c)])\n"
        func_code += f"    return result"
        
        return func_code
    
    def _encrypt_strings(self, code):
        """加密字符串
        
        Args:
            code: 源代码字符串
            
        Returns:
            str: 变换后的代码
        """
        # 寻找字符串字面量
        string_pattern = re.compile(r'"([^"]*)"|\'([^\']*)\'')
        
        # 收集解密函数和变量定义
        decrypt_functions = []
        var_definitions = []
        var_map = {}
        
        def replace_string(match):
            # 获取字符串内容
            if match.group(1):
                string = match.group(1)
            else:
                string = match.group(2)
            
            # 只处理非空字符串
            if not string:
                return match.group(0)
            
            # 检查是否已经处理过这个字符串
            if string in var_map:
                return var_map[string]
            
            # 加密字符串
            encrypted_data, key, iv = self._encrypt_string(string)
            
            # 生成解密代码
            var_name = f"_str_{random.randint(1000, 9999)}"
            decrypt_func = f"_decrypt_{random.randint(1000, 9999)}"
            
            # 转换为字节列表表示
            encrypted_hex = encrypted_data.hex()
            key_hex = key.hex()
            iv_hex = iv.hex()
            
            # 生成解密函数
            decrypt_code = f"""
def {decrypt_func}():
    import binascii
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding

    encrypted_data = binascii.unhexlify('{encrypted_hex}')
    key = binascii.unhexlify('{key_hex}')
    iv = binascii.unhexlify('{iv_hex}')

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted.decode('utf-8')

"""
            decrypt_functions.append(decrypt_code)
            
            # 生成变量定义
            var_def = f"{var_name} = {decrypt_func}()\n"
            var_definitions.append(var_def)
            
            # 保存映射
            var_map[string] = var_name
            
            return var_name
        
        # 替换字符串
        transformed_code = string_pattern.sub(replace_string, code)
        
        # 组合所有部分
        all_code = ''.join(decrypt_functions) + ''.join(var_definitions) + transformed_code
        
        return all_code
    
    def _encrypt_string(self, string):
        """加密字符串
        
        Args:
            string: 要加密的字符串
            
        Returns:
            tuple: (encrypted_data, key, iv) - 加密数据、密钥和初始化向量
        """
        # 生成随机密钥和初始化向量
        key = os.urandom(32)  # AES-256 需要 32 字节密钥
        iv = os.urandom(16)   # AES 块大小为 16 字节
        
        # 填充数据
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(string.encode('utf-8')) + padder.finalize()
        
        # 创建加密器
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # 加密数据
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        return encrypted_data, key, iv
