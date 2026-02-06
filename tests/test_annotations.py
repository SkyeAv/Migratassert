"""Tests for annotations mapper."""

import pytest
from migratassert.annotations import map_annotations, normalize_annotation_name


class TestNormalizeAnnotationName:
  def test_known_mappings(self):
    assert normalize_annotation_name("p_value") == "p value"
    assert normalize_annotation_name("sample_size") == "sample size"
    assert normalize_annotation_name("notes") == "miscellaneous notes"

  def test_default_underscore_replacement(self):
    assert normalize_annotation_name("custom_field") == "custom field"
    assert normalize_annotation_name("my_annotation") == "my annotation"


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

    # Result is now a list of annotation objects
    assert isinstance(result.mapped, list)
    assert len(result.mapped) == 2

    # Find p_value annotation
    p_val = next(a for a in result.mapped if a["annotation"] == "p value")
    assert p_val["method"] == "column"
    assert p_val["encoding"] == "pval"

    # Find sample_size annotation
    sample = next(a for a in result.mapped if a["annotation"] == "sample size")
    assert sample["method"] == "value"
    assert sample["encoding"] == 1000

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

    assert len(result.mapped) == 1
    log_pval = result.mapped[0]
    assert log_pval["annotation"] == "log pvalue"
    assert log_pval["transformations"] == [
      {"function": "log", "arguments": ["values", 10]}
    ]

  def test_maps_plain_value_annotation(self):
    """Plain string values become method: value annotations."""
    v440 = {
      "notes": "Some notes about this data",
    }
    result = map_annotations(v440)

    assert len(result.mapped) == 1
    notes = result.mapped[0]
    assert notes["annotation"] == "miscellaneous notes"
    assert notes["method"] == "value"
    assert notes["encoding"] == "Some notes about this data"
