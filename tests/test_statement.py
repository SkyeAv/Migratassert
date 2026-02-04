"""Tests for statement mapper."""

import pytest
from migratassert.statement import map_statement


class TestMapStatement:
  def test_maps_subject_object_predicate(self):
    v440 = {
      "triple_subject": {
        "encoding_method": "column",
        "value_for_encoding": "gene",
      },
      "triple_predicate": {
        "encoding_method": "value",
        "value_for_encoding": "biolink:related_to",
      },
      "triple_object": {
        "encoding_method": "column",
        "value_for_encoding": "disease",
      },
    }
    result = map_statement(v440)
    assert result.mapped["subject"]["method"] == "column"
    assert result.mapped["subject"]["encoding"] == "gene"
    assert result.mapped["predicate"] == "biolink:related_to"
    assert result.mapped["object"]["method"] == "column"
    assert result.mapped["object"]["encoding"] == "disease"

  def test_predicate_extracts_string_value(self):
    v440 = {
      "triple_predicate": {
        "encoding_method": "value",
        "value_for_encoding": "biolink:causes",
      },
    }
    result = map_statement(v440)
    assert result.mapped["predicate"] == "biolink:causes"

  def test_maps_subject_with_hyperparameters(self):
    v440 = {
      "triple_subject": {
        "encoding_method": "column",
        "value_for_encoding": "A",
        "mapping_hyperparameters": {
          "in_this_organism": "NCBITaxon:9606",
          "classes_to_prioritize": ["biolink:Gene"],
        },
      },
      "triple_predicate": {"value_for_encoding": "biolink:related_to"},
      "triple_object": {
        "encoding_method": "column",
        "value_for_encoding": "B",
      },
    }
    result = map_statement(v440)
    assert result.mapped["subject"]["taxon"] == 9606
    assert result.mapped["subject"]["prioritize"] == ["biolink:Gene"]
