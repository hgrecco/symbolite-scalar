"""
    symbolite.scalar.abstract
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Function and values for test_scalar operations.

    :copyright: 2023 by Symbolite Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import annotations

import dataclasses
import functools

from symbolite.core.operands import Function
from symbolite.symbol.abstract import Symbol

NAMESPACE = "libscalar"


_functions = {
    "abs": 1,
    "acos": 1,
    "acosh": 1,
    "asin": 1,
    "asinh": 1,
    "atan": 1,
    "atan2": 2,
    "atanh": 1,
    "ceil": 1,
    "comb": 2,
    "copysign": 2,
    "cos": 1,
    "cosh": 1,
    "degrees": 1,
    "erf": 1,
    "erfc": 1,
    "exp": 1,
    "expm1": 1,
    "fabs": 1,
    "factorial": 1,
    "floor": 1,
    "fmod": 2,
    "frexp": 1,
    "gamma": 1,
    "gcd": None,  # 1 to ---
    "hypot": None,  # 1 to ---
    "isclose": None,  # 2, 3, 4
    "isfinite": 1,
    "isinf": 1,
    "isnan": 1,
    "isqrt": 1,
    "lcm": None,  # 1 to ---
    "ldexp": 2,
    "lgamma": 1,
    "log": None,  # 1 or 2
    "log10": 1,
    "log1p": 1,
    "log2": 1,
    "modf": 1,
    "nextafter": 2,
    "perm": None,  # 1 or 2
    "pow": 2,
    "radians": 1,
    "remainder": 2,
    "sin": 1,
    "sinh": 1,
    "sqrt": 1,
    "tan": 1,
    "tanh": 1,
    "trunc": 1,
    "ulp": 1,
}

_values = ("e", "inf", "pi", "nan", "tau")


@dataclasses.dataclass(frozen=True)
class Scalar(Symbol):
    """A user defined symbol."""

    pass


__all__ = sorted(_values + tuple(_functions.keys()) + ("Scalar",))


def __dir__():
    return __all__


@functools.lru_cache(maxsize=None)
def __getattr__(name):
    if name not in __all__:
        raise AttributeError(f"module {__name__} has no attribute {name}")

    elif name in _functions:
        return Function(name, NAMESPACE, arity=_functions[name])
    else:
        return Scalar(name, NAMESPACE)
