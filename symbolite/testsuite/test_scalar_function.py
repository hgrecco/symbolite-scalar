import inspect

import pytest
from symbolite.core.translators import as_function, get_lib_implementation

from symbolite.scalar import abstract as scalar

all_impl = get_lib_implementation("scalar")

x, y, z = map(scalar.Scalar, "x y z".split())


@pytest.mark.parametrize(
    "expr",
    [
        x + y,
        x - y,
        x * y,
        x / y,
        x**y,
        x // y,
    ],
)
@pytest.mark.parametrize("libscalar", all_impl.values(), ids=all_impl.keys())
def test_known_symbols(expr, libscalar):
    f = as_function(expr, "my_function", ("x", "y"), libscalar=libscalar)
    assert f.__name__ == "my_function"
    assert expr.subs_by_name(x=2, y=3).eval(libscalar=libscalar) == f(2, 3)
    assert tuple(inspect.signature(f).parameters.keys()) == ("x", "y")


@pytest.mark.parametrize(
    "expr,replaced",
    [
        (x + scalar.cos(y), 2 + scalar.cos(3)),
        (x + scalar.pi * y, 2 + scalar.pi * 3),
    ],
)
@pytest.mark.parametrize("libscalar", all_impl.values(), ids=all_impl.keys())
def test_lib_symbols(expr, replaced, libscalar):
    f = as_function(expr, "my_function", ("x", "y"), libscalar=libscalar)
    value = f(2, 3)
    assert f.__name__ == "my_function"
    assert expr.subs_by_name(x=2, y=3).eval(libscalar=libscalar) == value
    assert tuple(inspect.signature(f).parameters.keys()) == ("x", "y")


@pytest.mark.parametrize(
    "expr,namespace,result",
    [
        (
            x + scalar.pi * scalar.cos(y),
            None,
            {
                "x",
                "y",
                f"{scalar.NAMESPACE}.cos",
                f"{scalar.NAMESPACE}.pi",
                "libsymbol.__mul__",
                "libsymbol.__add__",
            },
        ),
        (x + scalar.pi * scalar.cos(y), "", {"x", "y"}),
        (
            x + scalar.pi * scalar.cos(y),
            "libscalar",
            {f"{scalar.NAMESPACE}.cos", f"{scalar.NAMESPACE}.pi"},
        ),
    ],
)
def test_list_symbols(expr, namespace, result):
    assert expr.symbol_names(namespace) == result
