"""Test that sections are properly transformed from v4.4.0 to TC3."""

from migratassert.transform import transform_config


def test_sections_transform_triple_to_statement():
  """Sections with triple should be transformed to statement."""
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
      "sections": [
        {
          "triple": {
            "triple_subject": {
              "encoding_method": "column",
              "value_for_encoding": "gene_col",
            },
            "triple_predicate": {"value_for_encoding": "biolink:associated_with"},
            "triple_object": {
              "encoding_method": "column",
              "value_for_encoding": "disease_col",
            },
          }
        }
      ],
    }
  }
  result = transform_config(v440)
  tc3 = result.config["template"]

  # Main template transformed
  assert "statement" in tc3
  assert tc3["statement"]["subject"]["encoding"] == "A"

  # Sections should also be transformed
  assert "sections" in tc3
  section = tc3["sections"][0]

  # Check that triple was transformed to statement
  assert "statement" in section, f"Section should have 'statement', got: {section.keys()}"
  assert section["statement"]["subject"]["encoding"] == "gene_col"
  assert section["statement"]["predicate"] == "associated_with"
  assert section["statement"]["object"]["encoding"] == "disease_col"

  # Check that triple keys no longer exist
  assert "triple" not in section


def test_sections_transform_attributes_to_annotations():
  """Sections with attributes should be transformed to annotations."""
  v440 = {
    "template": {
      "triple": {
        "triple_predicate": {"value_for_encoding": "biolink:related_to"},
      },
      "sections": [
        {
          "attributes": {
            "p_value": {
              "encoding_method": "column",
              "value_for_encoding": "pval",
            }
          }
        }
      ],
    }
  }
  result = transform_config(v440)
  section = result.config["template"]["sections"][0]

  # Check that attributes was transformed to annotations
  assert "annotations" in section, f"Section should have 'annotations', got: {section.keys()}"
  p_value = next(a for a in section["annotations"] if a["annotation"] == "p value")
  assert p_value["encoding"] == "pval"

  # Check that attributes key no longer exists
  assert "attributes" not in section


def test_sections_with_nested_mappings():
  """Sections with nested NodeEncoding mappings should be transformed."""
  v440 = {
    "template": {
      "triple": {
        "triple_predicate": {"value_for_encoding": "biolink:related_to"},
      },
      "sections": [
        {
          "triple": {
            "triple_subject": {
              "encoding_method": "column",
              "value_for_encoding": "gene",
              "mapping_hyperparameters": {
                "in_this_organism": "NCBITaxon:9606",
                "classes_to_prioritize": ["biolink:Gene"],
                "substrings_to_remove": ["(obsolete)"],
              },
            },
            "triple_predicate": {"value_for_encoding": "biolink:treats"},
            "triple_object": {
              "encoding_method": "column",
              "value_for_encoding": "disease",
            },
          }
        }
      ],
    }
  }
  result = transform_config(v440)
  section = result.config["template"]["sections"][0]

  subject = section["statement"]["subject"]
  assert subject["method"] == "column"
  assert subject["encoding"] == "gene"
  assert subject["taxon"] == 9606  # NCBITaxon: prefix removed, converted to int
  assert subject["prioritize"] == ["Gene"]  # biolink: prefix removed
  assert subject["remove"] == ["(obsolete)"]
