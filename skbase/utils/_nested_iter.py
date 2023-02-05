#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Functionality for working with nested sequences."""
import collections
from typing import List

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = [
    "_flatten",
    "_is_flat",
    "_remove_single",
    "_unflat_len",
    "_unflatten",
]


def _remove_single(x):
    """Remove tuple wrapping from singleton.

    If the input has length 1, then the single value is extracted from the input.
    Otherwise, the input is returned unchanged.

    Parameters
    ----------
    x : Sequence
        The sequence to remove a singleton value from.

    Returns
    -------
    Any
        The singleton value of x if x[0] is a singleton, otherwise x.

    Examples
    --------
    >>> from skbase.utils._nested_iter import _remove_single
    >>> _remove_single([1])
    1
    >>> _remove_single([1, 2, 3])
    [1, 2, 3]
    """
    if len(x) == 1:
        return x[0]
    else:
        return x


def _flatten(obj):
    """Flatten nested list/tuple structure.

    Converts a nested iterable or sequence to a flat output iterable/sequence
    with the same and order of elements.

    Parameters
    ----------
    obj : Any
        The object to be flattened from a nested iterable/sequence structure.

    Returns
    -------
    Sequence or Iterable
        flat iterable/sequence, containing non-list/tuple elements in obj in
        same order as in obj.

    Example
    -------
    >>> from skbase.utils._nested_iter import _flatten
    >>> _flatten([1, 2, [3, (4, 5)], 6])
    [1, 2, 3, 4, 5, 6]
    """
    if not isinstance(obj, (collections.abc.Iterable, collections.abc.Sequence)):
        return [obj]
    else:
        return type(obj)([y for x in obj for y in _flatten(x)])


def _unflatten(obj, template):
    """Invert flattening given given template for nested list/tuple structure.

    Converts an input list or tuple to a nested structure as provided in `template`
    while preserving the order of elements in the input.

    Parameters
    ----------
    obj : list or tuple
        The object to be unflattened.
    template : nested list/tuple structure
        Number of non-list/tuple elements of obj and template must be equal.

    Returns
    -------
    list or tuple
        Input coerced to have elements with nested list/tuples structure exactly
        as `template` and elements in sequence exactly as `obj`.

    Example
    -------
    >>> from skbase.utils._nested_iter import _unflatten
    >>> _unflatten([1, 2, 3, 4, 5, 6], [6, 3, [5, (2, 4)], 1])
    [1, 2, [3, (4, 5)], 6]
    """
    if not isinstance(template, (list, tuple)):
        return obj[0]

    list_or_tuple = type(template)
    ls = [_unflat_len(x) for x in template]
    for i in range(1, len(ls)):
        ls[i] += ls[i - 1]
    ls = [0] + ls

    res = [_unflatten(obj[ls[i] : ls[i + 1]], template[i]) for i in range(len(ls) - 1)]

    return list_or_tuple(res)


def _unflat_len(obj):
    """Return number of elements in nested iterable or sequence structure.

    Determines the total number of elements in a nested iterable/sequence structure.
    Input that is not a iterable or sequence is considered to have length 1.

    Parameters
    ----------
    obj : Any
        Object to determine the unflat length.

    Returns
    -------
    int
        The unflat length of the input.

    Examples
    --------
    >>> from skbase.utils._nested_iter import _unflat_len
    >>> _unflat_len(7)
    1
    >>> _unflat_len((1, 2))
    2
    >>> _unflat_len([1, (2, 3), 4, 5])
    5
    """
    if not isinstance(obj, (collections.abc.Iterable, collections.abc.Sequence)):
        return 1
    else:
        return sum([_unflat_len(x) for x in obj])


def _is_flat(obj):
    """Check whether iterable or sequence is flat.

    If any elements are iterables or sequences the object is considered to not be flat.

    Parameters
    ----------
    obj : Any
        The object to check to see if it is flat (does not have nested iterable).

    Returns
    -------
    bool
        Whether or not the input `obj` contains nested iterables.

    Examples
    --------
    >>> from skbase.utils._nested_iter import _is_flat
    >>> _is_flat([1, 2, 3, 4, 5])
    True
    >>> _is_flat([1, (2, 3), 4, 5])
    False
    """
    elements_flat = (
        isinstance(x, (collections.abc.Iterable, collections.abc.Sequence)) for x in obj
    )
    return not any(elements_flat)
