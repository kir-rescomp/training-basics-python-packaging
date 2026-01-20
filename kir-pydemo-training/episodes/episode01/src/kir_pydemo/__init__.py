"""kir-pydemo: A demonstration package for DNA sequence analysis."""

__version__ = "0.1.0"

# Import main functions to make them easily accessible
from kir_pydemo.sequence import gc_content, reverse_complement

__all__ = ["gc_content", "reverse_complement"]
