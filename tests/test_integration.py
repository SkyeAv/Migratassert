"""Integration tests for end-to-end transformation."""

import pytest
from migratassert.transform import transform_config


class TestFullTransformation:
  def test_transforms_full_config(self, v440_full_config, tc3_expected_config):
    """Test that full v4.4.0 config transforms to expected TC3 output."""
    result = transform_config(v440_full_config)
    tc3 = result.config["template"]
    expected = tc3_expected_config["template"]

    assert tc3["syntax"] == "TC3"

    assert tc3["source"]["url"] == expected["source"]["url"]
    assert tc3["source"]["local"] == expected["source"]["local"]
    assert tc3["source"]["kind"] == expected["source"]["kind"]
    assert tc3["source"]["sheet"] == expected["source"]["sheet"]
    assert tc3["source"]["row_slice"] == expected["source"]["row_slice"]
    assert tc3["source"]["reindex"] == expected["source"]["reindex"]

    assert tc3["statement"]["subject"]["method"] == expected["statement"]["subject"]["method"]
    assert tc3["statement"]["subject"]["taxon"] == expected["statement"]["subject"]["taxon"]
    assert tc3["statement"]["predicate"] == expected["statement"]["predicate"]
    assert tc3["statement"]["object"]["prioritize"] == expected["statement"]["object"]["prioritize"]

    assert tc3["provenance"]["repo"] == expected["provenance"]["repo"]
    assert tc3["provenance"]["contributors"][0]["name"] == expected["provenance"]["contributors"][0]["name"]

    # annotations is now a list of objects with 'annotation' key
    assert isinstance(tc3["annotations"], list)
    assert len(tc3["annotations"]) == len(expected["annotations"])

    # Find p_value annotation and verify transformations
    p_val_tc3 = next(a for a in tc3["annotations"] if a["annotation"] == "p value")
    p_val_exp = next(a for a in expected["annotations"] if a["annotation"] == "p value")
    assert p_val_tc3["transformations"] == p_val_exp["transformations"]
