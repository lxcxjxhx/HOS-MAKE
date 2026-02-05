"""HOS-MAKE - 多语言代码加密系统"""

__version__ = "0.5.0"
__author__ = "HOS Team"
__description__ = "多语言代码加密系统，支持Python、C/C++、Rust、Go、ARM和WebAssembly"

from hos.analyzer import analyze
from hos.transformer import transform
from hos.runtime import protect

__all__ = ["analyze", "transform", "protect"]
