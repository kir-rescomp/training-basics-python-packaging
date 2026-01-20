"""DNA sequence analysis utilities."""


def gc_content(sequence: str) -> float:
    """
    Calculate GC content of a DNA sequence.
    
    Parameters
    ----------
    sequence : str
        DNA sequence containing A, T, G, C nucleotides
    
    Returns
    -------
    float
        GC content as a percentage (0-100)
    
    Examples
    --------
    >>> gc_content("ATGC")
    50.0
    >>> gc_content("AAAA")
    0.0
    """
    if not sequence:
        raise ValueError("Sequence cannot be empty")
    
    sequence = sequence.upper()
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    
    return (g_count + c_count) / len(sequence) * 100


def reverse_complement(sequence: str) -> str:
    """
    Get the reverse complement of a DNA sequence.
    
    Parameters
    ----------
    sequence : str
        DNA sequence containing A, T, G, C nucleotides
    
    Returns
    -------
    str
        Reverse complement of the input sequence
    
    Examples
    --------
    >>> reverse_complement("ATGC")
    'GCAT'
    >>> reverse_complement("AAAA")
    'TTTT'
    """
    complement_map = {
        'A': 'T', 'T': 'A',
        'G': 'C', 'C': 'G',
        'a': 't', 't': 'a',
        'g': 'c', 'c': 'g'
    }
    
    return ''.join(complement_map.get(base, base) for base in reversed(sequence))
