"""命令行工具主文件"""

import click
import os
import sys
from tqdm import tqdm
from hos.language.processor_factory import ProcessorFactory
from hos.ai import AIStrategyGenerator

@click.group()
def cli():
    """HOS-MAKE - AI驱动的代码加密系统"""
    pass

@cli.command()
@click.option('--input', '-i', required=True, help='输入文件或目录')
@click.option('--output', '-o', required=True, help='输出文件或目录')
@click.option('--level', '-l', default='medium', type=click.Choice(['low', 'medium', 'high']), help='混淆强度')
@click.option('--mode', '-m', default='balanced', type=click.Choice(['performance', 'balanced', 'security']), help='性能模式')
@click.option('--provider', '-p', default='local', type=click.Choice(['local', 'openai', 'anthropic', 'google']), help='AI provider')
@click.option('--api-key', '-k', help='API key for AI provider')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
def protect(input, output, level, mode, provider, api_key, verbose):
    """加密代码文件或目录"""
    # 检查输入是否存在
    if not os.path.exists(input):
        click.echo(f"错误: 输入文件或目录 '{input}' 不存在", err=True)
        sys.exit(1)
    
    # 确定输入类型
    is_dir = os.path.isdir(input)
    
    # 确保输出目录存在
    if is_dir:
        if not os.path.exists(output):
            os.makedirs(output)
    else:
        output_dir = os.path.dirname(output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    # 初始化AI策略生成器和处理器工厂
    ai_generator = AIStrategyGenerator(provider=provider, api_key=api_key)
    factory = ProcessorFactory()
    
    # 处理输入
    if is_dir:
        # 处理目录
        files = []
        for root, _, filenames in os.walk(input):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                try:
                    # 检测文件语言
                    language = factory.detector.detect_from_file(file_path)
                    if factory.detector.is_supported(language):
                        files.append(file_path)
                except Exception:
                    pass
        
        if not files:
            click.echo(f"警告: 目录 '{input}' 中没有找到支持的文件", err=True)
            sys.exit(0)
        
        # 处理每个文件
        with tqdm(total=len(files), desc="加密文件", unit="file") as pbar:
            for file_path in files:
                # 计算相对路径
                rel_path = os.path.relpath(file_path, input)
                output_path = os.path.join(output, rel_path)
                
                # 确保输出目录存在
                output_file_dir = os.path.dirname(output_path)
                if not os.path.exists(output_file_dir):
                    os.makedirs(output_file_dir)
                
                # 处理文件
                process_file(file_path, output_path, level, mode, verbose, ai_generator, factory)
                pbar.update(1)
    else:
        # 处理单个文件
        process_file(input, output, level, mode, verbose, ai_generator, factory)
    
    click.echo(f"\n加密完成! 结果保存在 '{output}'")

def process_file(input_path, output_path, level, mode, verbose, ai_generator, factory):
    """处理单个文件"""
    try:
        # 读取文件
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        if verbose:
            click.echo(f"\n处理文件: {input_path}")
            click.echo(f"输出文件: {output_path}")
        
        # 获取语言处理器
        processor = factory.get_processor_from_file(input_path)
        language = processor.get_language_name()
        
        if verbose:
            click.echo(f"检测到语言: {language}")
        
        # 分析代码
        if verbose:
            click.echo("分析代码...")
        analysis = processor.analyze(code)
        
        # 生成混淆策略
        if verbose:
            click.echo("生成混淆策略...")
        strategy = ai_generator.generate_strategy(analysis, mode)
        
        # 根据强度调整策略
        if level == 'low':
            strategy.set_strength(0.3)
        elif level == 'medium':
            strategy.set_strength(0.5)
        else:  # high
            strategy.set_strength(0.8)
        
        # 转换代码
        if verbose:
            click.echo("转换代码...")
        transformed_code = processor.transform(code, strategy)
        
        # 写入输出文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transformed_code)
        
        if verbose:
            click.echo("加密成功!")
            
    except Exception as e:
        click.echo(f"错误处理文件 '{input_path}': {str(e)}", err=True)

@cli.command()
@click.option('--file', '-f', required=True, help='要分析的代码文件')
@click.option('--output', '-o', help='分析结果输出文件')
def analyze_cmd(file, output):
    """分析代码文件"""
    # 检查文件是否存在
    if not os.path.exists(file):
        click.echo(f"错误: 文件 '{file}' 不存在", err=True)
        sys.exit(1)
    
    # 读取文件
    with open(file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # 初始化处理器工厂
    factory = ProcessorFactory()
    
    # 分析代码
    click.echo(f"分析文件: {file}")
    try:
        # 获取语言处理器
        processor = factory.get_processor_from_file(file)
        language = processor.get_language_name()
        click.echo(f"检测到语言: {language}")
        
        # 分析代码
        analysis = processor.analyze(code)
        
        # 输出分析结果
        if output:
            import json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            click.echo(f"分析结果已保存到: {output}")
        else:
            # 打印简要分析结果
            click.echo("\n=== 分析结果 ===")
            click.echo(f"代码行数: {analysis.get('line_count', 0)}")
            click.echo(f"代码大小: {analysis.get('code_size', 0)} 字节")
            click.echo(f"函数数量: {len(analysis.get('ast', {}).get('functions', []))}")
            click.echo(f"类数量: {len(analysis.get('ast', {}).get('classes', []))}")
            click.echo(f"热路径数量: {len(analysis.get('hot_paths', []))}")
            click.echo(f"敏感度评分: {analysis.get('sensitivity', {}).get('sensitivity_score', 0):.2f}")
            click.echo(f"安全价值评分: {analysis.get('security_score', 0):.2f}")
    except Exception as e:
        click.echo(f"错误分析文件 '{file}': {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def version():
    """显示版本信息"""
    from hos import __version__, __description__
    click.echo(f"HOS-MAKE {__version__}")
    click.echo(f"{__description__}")

@cli.command()
def help_cmd():
    """显示帮助信息"""
    cli.main(['--help'])

if __name__ == '__main__':
    cli()
