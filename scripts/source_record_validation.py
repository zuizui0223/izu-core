"""Complete, finite comparison of JSON-like audit receipts.

Callers retain their scientific tolerance and contract-specific diagnostics.
This helper neither recalculates results nor rewrites admitted source records.
"""
import numpy as np


def equal_source_record(a, b, *, atol):
    """Compare every field in order, rejecting nonfinite numbers and bool/int swaps."""
    if isinstance(a, dict):
        return (isinstance(b, dict) and set(a) == set(b)
                and all(equal_source_record(a[k], b[k], atol=atol) for k in a))
    if isinstance(a, list):
        return (isinstance(b, list) and len(a) == len(b)
                and all(equal_source_record(x, y, atol=atol) for x, y in zip(a, b)))
    if type(a) is bool or type(b) is bool:
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return np.isfinite(a) and np.isfinite(b) and abs(a - b) <= atol
    return type(a) is type(b) and a == b
