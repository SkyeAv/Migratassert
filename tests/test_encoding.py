"""Tests for encoding mapper."""

import pytest
from migratassert.encoding import extract_taxon_id, map_transformations


class TestExtractTaxonId:
  def test_parses_ncbitaxon_curie(self):
    assert extract_taxon_id("NCBITaxon:9606") == 9606

  def test_parses_plain_integer_string(self):
    assert extract_taxon_id("9606") == 9606

  def test_parses_other_prefix(self):
    assert extract_taxon_id("taxon:10090") == 10090


class TestMapTransformations:
  def test_renames_attribute_to_function(self):
    v440 = {"attribute": "multiply", "arguments": ["values", 0.05]}
    result = map_transformations(v440)
    assert result == [{"function": "multiply", "arguments": ["values", 0.05]}]

  def test_handles_list_of_transformations(self):
    v440 = [
      {"attribute": "log", "arguments": ["values"]},
      {"attribute": "round", "arguments": ["values", 2]},
    ]
    result = map_transformations(v440)
    assert len(result) == 2
    assert result[0]["function"] == "log"
    assert result[1]["function"] == "round"

  def test_returns_empty_list_for_none(self):
    assert map_transformations(None) == []
