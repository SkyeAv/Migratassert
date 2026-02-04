"""Tests for transform orchestration."""

import pytest
from migratassert.transform import transform_config


class TestTransformConfig:
  def test_adds_syntax_tc3(self):
    v440 = {"template": {}}
    result = transform_config(v440)
    assert result.config["template"]["syntax"] == "TC3"

  def test_transforms_all_blocks(self):
    v440 = {
      "template": {
        "location": {
          "posix_filepath": "/data/file.csv",
          "download_hyperparameters": {"file_extension": "csv"},
        },
        "triple": {
          "triple_subject": {
            "encoding_method": "column",
            "value_for_encoding": "A",
          },
          "triple_predicate": {"value_for_encoding": "biolink:related_to"},
          "triple_object": {
            "encoding_method": "column",
            "value_for_encoding": "B",
          },
        },
        "provenance": {
          "publication": "PMC:12345",
          "config_curator_name": "Test User",
        },
        "attributes": {
          "p_value": {
            "encoding_method": "column",
            "value_for_encoding": "pval",
          },
        },
        "reindexing": [
          {"column": "pval", "comparison": "lt", "value_for_comparison": 0.05}
        ],
      }
    }
    result = transform_config(v440)
    tc3 = result.config["template"]

    assert tc3["syntax"] == "TC3"
    assert tc3["source"]["local"] == "/data/file.csv"
    assert tc3["source"]["kind"] == "text"
    assert tc3["source"]["reindex"][0]["comparator"] == 0.05
    assert tc3["statement"]["subject"]["encoding"] == "A"
    assert tc3["statement"]["predicate"] == "biolink:related_to"
    assert tc3["provenance"]["repo"] == "PMC"
    assert tc3["annotations"]["p_value"]["method"] == "column"

  def test_preserves_sections(self):
    v440 = {
      "template": {
        "triple": {
          "triple_predicate": {"value_for_encoding": "biolink:related_to"},
        },
        "sections": [
          {"triple": {"triple_predicate": {"value_for_encoding": "biolink:causes"}}}
        ],
      }
    }
    result = transform_config(v440)
    assert "sections" in result.config["template"]
    assert len(result.config["template"]["sections"]) == 1
