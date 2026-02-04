"""Tests for encoding mapper."""

import pytest
from migratassert.encoding import extract_taxon_id, map_transformations, map_node_encoding


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


class TestMapNodeEncoding:
  def test_maps_basic_fields(self):
    v440 = {
      "encoding_method": "column",
      "value_for_encoding": "gene_symbol",
    }
    result = map_node_encoding(v440)
    assert result.mapped["method"] == "column"
    assert result.mapped["encoding"] == "gene_symbol"

  def test_maps_mapping_hyperparameters(self):
    v440 = {
      "encoding_method": "column",
      "value_for_encoding": "A",
      "mapping_hyperparameters": {
        "in_this_organism": "NCBITaxon:9606",
        "classes_to_prioritize": ["biolink:Gene"],
        "classes_to_avoid": ["biolink:Protein"],
        "prefix": "HGNC:",
        "suffix": "_human",
        "substrings_to_remove": ["(obsolete)"],
        "regular_expressions": [{"pattern": "\\s+", "replacement": "_"}],
        "explode_by_delimiter": ";",
      },
    }
    result = map_node_encoding(v440)
    assert result.mapped["taxon"] == 9606
    assert result.mapped["prioritize"] == ["biolink:Gene"]
    assert result.mapped["avoid"] == ["biolink:Protein"]
    assert result.mapped["prefix"] == "HGNC:"
    assert result.mapped["suffix"] == "_human"
    assert result.mapped["remove"] == ["(obsolete)"]
    assert result.mapped["regex"] == [{"pattern": "\\s+", "replacement": "_"}]
    assert result.mapped["explode_by"] == ";"

  def test_maps_transformations(self):
    v440 = {
      "encoding_method": "column",
      "value_for_encoding": "pvalue",
      "math_module_transformations": {"attribute": "log", "arguments": ["values"]},
    }
    result = map_node_encoding(v440)
    assert result.mapped["transformations"] == [
      {"function": "log", "arguments": ["values"]}
    ]

  def test_tracks_dropped_fields(self):
    v440 = {
      "encoding_method": "column",
      "value_for_encoding": "A",
      "mapping_hyperparameters": {
        "how_to_fill_column": "forward",
        "unknown_field": "value",
      },
    }
    result = map_node_encoding(v440, field_prefix="subject.")
    assert "subject.how_to_fill_column" in result.dropped
    assert "subject.unknown_field" in result.dropped
