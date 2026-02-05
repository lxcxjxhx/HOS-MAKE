"""HOS系统测试文件"""

import hos

def test_analyze():
    """测试代码分析功能"""
    # 测试代码
    test_code = '''
def add(a, b):
    return a + b

def multiply(a, b):
    result = 0
    for i in range(b):
        result += a
    return result

# 测试函数
x = 5
y = 10
print(add(x, y))
print(multiply(x, y))
'''
    
    print("=== 测试代码分析 ===")
    analysis_result = hos.analyze(test_code)
    print(f"代码大小: {analysis_result['code_size']}")
    print(f"行数: {analysis_result['line_count']}")
    print(f"函数数量: {len(analysis_result['ast']['functions'])}")
    print(f"安全评分: {analysis_result['security_score']}")
    print(f"热路径数量: {len(analysis_result['hot_paths'])}")
    print(f"敏感度评分: {analysis_result['sensitivity']['sensitivity_score']}")
    print("✅ 代码分析测试通过")

def test_transform():
    """测试代码变换功能"""
    # 测试代码
    test_code = '''
def add(a, b):
    return a + b

def multiply(a, b):
    result = 0
    for i in range(b):
        result += a
    return result
'''
    
    print("\n=== 测试代码变换 ===")
    from hos.ai.strategy import ConfusionStrategy
    
    # 创建混淆策略
    strategy = ConfusionStrategy()
    strategy.set_strength(0.5)
    strategy.control_flow['flattening'] = True
    strategy.data['constant_splitting'] = True
    strategy.instruction['garbage_injection'] = True
    
    # 变换代码
    transformed_code = hos.transform(test_code, strategy)
    print(f"原始代码长度: {len(test_code)}")
    print(f"变换后代码长度: {len(transformed_code)}")
    print("变换后代码:")
    print(transformed_code[:500] + "..." if len(transformed_code) > 500 else transformed_code)
    print("✅ 代码变换测试通过")

def test_protect():
    """测试运行时保护功能"""
    # 测试代码
    test_code = '''
def add(a, b):
    return a + b

def multiply(a, b):
    result = 0
    for i in range(b):
        result += a
    return result
'''
    
    print("\n=== 测试运行时保护 ===")
    # 应用运行时保护
    protected_code = hos.protect(test_code, security_level='high')
    print(f"原始代码长度: {len(test_code)}")
    print(f"保护后代码长度: {len(protected_code)}")
    print("保护后代码:")
    print(protected_code[:500] + "..." if len(protected_code) > 500 else protected_code)
    print("✅ 运行时保护测试通过")

def test_full_workflow():
    """测试完整工作流"""
    # 测试代码
    test_code = '''
def add(a, b):
    return a + b

def multiply(a, b):
    result = 0
    for i in range(b):
        result += a
    return result

# 测试函数
x = 5
y = 10
print(add(x, y))
print(multiply(x, y))
'''
    
    print("\n=== 测试完整工作流 ===")
    
    # 1. 分析代码
    analysis_result = hos.analyze(test_code)
    
    # 2. 生成混淆策略
    from hos.ai.planner import StrategyPlanner
    planner = StrategyPlanner()
    strategy_plan = planner.plan_strategy(analysis_result, performance_mode='balanced', security_level='medium')
    
    # 3. 变换代码
    transformed_code = hos.transform(test_code, strategy_plan['strategy'])
    
    # 4. 应用运行时保护
    protected_code = hos.protect(transformed_code, security_level='medium')
    
    print(f"原始代码长度: {len(test_code)}")
    print(f"变换后代码长度: {len(transformed_code)}")
    print(f"保护后代码长度: {len(protected_code)}")
    print(f"策略安全评分: {strategy_plan['evaluation']['security_score']}")
    print(f"策略性能影响: {strategy_plan['evaluation']['performance_impact']}")
    print(f"策略平衡评分: {strategy_plan['evaluation']['balance_score']}")
    print("✅ 完整工作流测试通过")

if __name__ == "__main__":
    print("🚀 开始测试HOS系统")
    print(f"HOS版本: {hos.__version__}")
    print(f"描述: {hos.__description__}")
    
    try:
        test_analyze()
        test_transform()
        test_protect()
        test_full_workflow()
        print("\n🎉 所有测试通过！HOS系统工作正常")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()