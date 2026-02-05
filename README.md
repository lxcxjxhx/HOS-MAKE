# HOS - AI-Driven Code Encryption System

[中文版本](#hos-ai驱动的代码加密系统)

HOS (Honestly Of Selfish) is an AI-driven personalized code encryption system designed to "selfishly" protect developers' code.

## Core Features

- **AI-Dynamic Obfuscation Strategy**: Each user has unique "genes"
- **Intelligent Performance and Security Balance**: Automatically adjusts obfuscation strength
- **Powerful Runtime Protection**: Prevents debugging and memory tampering
- **Multi-language Support**: Initial version supports Python, with future extensions to C/C++, Rust, Go, etc.
- **Modular Design**: Easy to extend and customize

## System Architecture

```
                ┌────────────────────┐
                │   HOS AI Engine    │
                │ Obfuscation Strategy Generator │
                └─────────┬──────────┘
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
 ┌────────────┐   ┌──────────────┐   ┌──────────────┐
 │ Code Analysis Module │   │ Obfuscation Strategy Planner │   │ Performance Evaluation Predictor │
 └──────┬─────┘   └──────┬───────┘   └──────┬───────┘
        │                 │                  │
        └────────────┬────┴──────────────┬──┘
                     │                   │
               ┌──────────────┐   ┌──────────────┐
               │ Code Transformation Engine │   │ Runtime Protection Layer │
               └──────────────┘   └──────────────┘
```

## Quick Start

### Installation

```bash
# Using Poetry
poetry install

# Or using pip
pip install .
```

### Basic Usage

```bash
# Encrypt Python file
hos protect --input example.py --output protected_example.py

# Encrypt entire directory
hos protect --input src/ --output protected_src/

# Custom obfuscation strength
hos protect --input example.py --output protected_example.py --level high
```

## Directory Structure

```
hos/
├── analyzer/        # Code analysis module
├── ai/              # AI obfuscation strategy generation
├── transformer/     # Code transformation engine
├── runtime/         # Runtime protection layer
├── performance/     # Performance evaluation predictor
├── cli/             # Command line tools
└── utils/           # Utility functions
tests/               # Test files
docs/                # Documentation
examples/            # Example code
```

## Technology Stack

- **Core Language**: Python 3.8+
- **Code Analysis**: Tree-sitter
- **AI Model**: Fine-tuned model based on Code LLM
- **Build Tool**: Poetry
- **Testing Framework**: pytest

## Development Guide

### Running Tests

```bash
poetry run pytest
```

### Code Style Checking

```bash
poetry run black hos/ tests/
poetry run isort hos/ tests/
poetry run flake8 hos/ tests/
```

## Roadmap

- **v1.0**: Python code protection, basic obfuscation features
- **v2.0**: C/C++ support, based on LLVM IR-level obfuscation
- **v3.0**: Rust/Go support
- **v4.0**: Android NDK/ARM support
- **v5.0**: WASM protection

## Contribution

Contributions, issues, and feature requests are welcome!

## License

[MIT License](LICENSE)

---

# HOS - AI驱动的代码加密系统

[English Version](#hos-ai-driven-code-encryption-system)

## 核心特性

- **AI动态生成混淆策略**：每个用户都是不同的"基因"
- **智能性能与安全平衡**：自动调节混淆强度
- **强大的运行时保护**：防止调试、内存篡改
- **支持多语言**：初始版本支持Python，后续将扩展到C/C++、Rust、Go等
- **模块化设计**：易于扩展和定制

## 系统架构

```
                ┌────────────────────┐
                │   HOS AI Engine    │
                │ 混淆策略生成大模型 │
                └─────────┬──────────┘
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
 ┌────────────┐   ┌──────────────┐   ┌──────────────┐
 │ 代码分析模块 │   │ 混淆策略规划器 │   │ 性能评估预测器 │
 └──────┬─────┘   └──────┬───────┘   └──────┬───────┘
        │                 │                  │
        └────────────┬────┴──────────────┬──┘
                     │                   │
               ┌──────────────┐   ┌──────────────┐
               │ 代码变换引擎  │   │ 运行时保护层  │
               └──────────────┘   └──────────────┘
```

## 快速开始

### 安装

```bash
# 使用Poetry安装
poetry install

# 或者使用pip
pip install .
```

### 基本使用

```bash
# 加密Python文件
hos protect --input example.py --output protected_example.py

# 加密整个目录
hos protect --input src/ --output protected_src/

# 自定义混淆强度
hos protect --input example.py --output protected_example.py --level high
```

## 目录结构

```
hos/
├── analyzer/        # 代码分析模块
├── ai/              # AI混淆策略生成
├── transformer/     # 代码变换引擎
├── runtime/         # 运行时保护层
├── performance/     # 性能评估预测器
├── cli/             # 命令行工具
└── utils/           # 通用工具函数
tests/               # 测试文件
docs/                # 文档
examples/            # 示例代码
```

## 技术栈

- **核心语言**：Python 3.8+
- **代码分析**：Tree-sitter
- **AI模型**：基于Code LLM的微调模型
- **构建工具**：Poetry
- **测试框架**：pytest

## 开发指南

### 运行测试

```bash
poetry run pytest
```

### 代码风格检查

```bash
poetry run black hos/ tests/
poetry run isort hos/ tests/
poetry run flake8 hos/ tests/
```

## 路线图

- **v1.0**：Python代码保护，基础混淆功能
- **v2.0**：C/C++支持，基于LLVM IR级混淆
- **v3.0**：Rust/Go支持
- **v4.0**：Android NDK/ARM支持
- **v5.0**：WASM保护

## 贡献

欢迎贡献代码、报告问题或提出建议！

## 许可证

[MIT License](LICENSE)
