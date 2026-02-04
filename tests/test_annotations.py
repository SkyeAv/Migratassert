"""Tests for annotations mapper."""

import pytest
from migratassert.annotations import map_annotations


class TestMapAnnotations:
  def test_maps_attribute_with_encoding(self):
    v440 = {
      "p_value": {
        "encoding_method": "column",
        "value_for_encoding": "pval",
      },
      "sample_size": {
        "encoding_method": "value",
        "value_for_encoding": 1000,
      },
    }
    result = map_annotations(v440)
    assert result.mapped["p_value"]["method"] == "column"
    assert result.mapped["p_value"]["encoding"] == "pval"
    assert result.mapped["sample_size"]["method"] == "value"
    assert result.mapped["sample_size"]["encoding"] == 1000

  def test_maps_attribute_with_transformations(self):
    v440 = {
      "log_pvalue": {
        "encoding_method": "column",
        "value_for_encoding": "pval",
        "math_module_transformations": {
          "attribute": "log",
          "arguments": ["values", 10],
        },
      },
    }
    result = map_annotations(v440)
    assert result.mapped["log_pvalue"]["transformations"] == [
      {"function": "log", "arguments": ["values", 10]}
    ]
