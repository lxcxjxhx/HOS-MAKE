"""HOS - AI驱动的代码加密系统"""

__version__ = "0.1.0"
__author__ = "HOS Team"
__description__ = "AI驱动的个性化代码加密系统"

from hos.analyzer import analyze
from hos.transformer import transform
from hos.runtime import protect

__all__ = ["analyze", "transform", "protect"]
