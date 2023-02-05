#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests of the functionality for working with iterables.

tests in this module incdlue:

- test_format_seq_to_str: verify that _format_seq_to_str outputs expected format.
- test_format_seq_to_str_raises: verify _format_seq_to_str raises error on unexpected
  output.
- test_scalar_to_seq_expected_output: verify that _scalar_to_seq returns exepcted
  output.
- test_scalar_to_seq_raises: verify that _scalar_to_seq raises error when an
  invalid value is provided for sequence_type parameter.
"""
import pytest

from skbase.base import BaseEstimator, BaseObject
from skbase.utils._iter import _format_seq_to_str, _scalar_to_seq

__author__ = ["RNKuhns"]


def test_format_seq_to_str():
    """Test _format_seq_to_str returns expected output."""
    # Test basic functionality (including ability to handle str and non-str)
    seq = [1, 2, "3", 4]
    assert _format_seq_to_str(seq) == "1, 2, 3, 4"

    # Test use of last_sep
    assert _format_seq_to_str(seq, last_sep="and") == "1, 2, 3 and 4"
    assert _format_seq_to_str(seq, last_sep="or") == "1, 2, 3 or 4"

    # Test use of different sep argument
    assert _format_seq_to_str(seq, sep=";") == "1;2;3;4"

    # Verify things work with BaseObject and BaseEstimator instances
    seq = [BaseEstimator(), BaseObject(), 1]
    assert _format_seq_to_str(seq) == "BaseEstimator(), BaseObject(), 1"

    # Test use of last_sep
    assert (
        _format_seq_to_str(seq, last_sep="and") == "BaseEstimator(), BaseObject() and 1"
    )
    assert (
        _format_seq_to_str(seq, last_sep="or") == "BaseEstimator(), BaseObject() or 1"
    )

    # Test use of different sep argument
    assert _format_seq_to_str(seq, sep=";") == "BaseEstimator();BaseObject();1"

    # Test using remove_type_text keyword
    assert (
        _format_seq_to_str([list, tuple], remove_type_text=False)
        == "<class 'list'>, <class 'tuple'>"
    )
    assert _format_seq_to_str([list, tuple], remove_type_text=True) == "list, tuple"
    assert (
        _format_seq_to_str([list, tuple], last_sep="and", remove_type_text=True)
        == "list and tuple"
    )

    # Test with scalar inputs
    assert _format_seq_to_str(7) == "7"  # int, float, bool primitives cast to str
    assert _format_seq_to_str("some_str") == "some_str"
    # Verify that keywords don't affect output
    assert _format_seq_to_str(7, sep=";") == "7"
    assert _format_seq_to_str(7, last_sep="or") == "7"


def test_format_seq_to_str_raises():
    """Test _format_seq_to_str raises error when input is unexpected type."""
    with pytest.raises(
        ValueError, match="`seq` must be a sequence or scalar str, int, float or bool."
    ):
        _format_seq_to_str((c for c in [1, 2, 3]))

    with pytest.raises(
        ValueError, match="`seq` must be a sequence or scalar str, int, float or bool."
    ):
        _format_seq_to_str(object)


def test_scalar_to_seq_expected_output():
    """Test _scalar_to_seq returns expected output."""
    assert _scalar_to_seq(7) == (7,)
    # Verify it works with scalar classes and objects
    assert _scalar_to_seq(BaseObject) == (BaseObject,)
    assert _scalar_to_seq(BaseObject()) == (BaseObject(),)
    # Verify strings treated like scalar not sequence
    assert _scalar_to_seq("some_str") == ("some_str",)
    assert _scalar_to_seq("some_str", sequence_type=list) == ["some_str"]

    # Verify sequences returned unchanged
    assert _scalar_to_seq((1, 2)) == (1, 2)


def test_scalar_to_seq_raises():
    """Test scalar_to_seq raises error when `sequence_type` is unexpected type."""
    with pytest.raises(
        ValueError,
        match="`sequence_type` must be a subclass of collections.abc.Sequence.",
    ):
        _scalar_to_seq(7, sequence_type=int)

    with pytest.raises(
        ValueError,
        match="`sequence_type` must be a subclass of collections.abc.Sequence.",
    ):
        _scalar_to_seq(7, sequence_type=dict)
