"""Tests for encoding mapper."""

import pytest
from migratassert.encoding import extract_taxon_id


class TestExtractTaxonId:
  def test_parses_ncbitaxon_curie(self):
    assert extract_taxon_id("NCBITaxon:9606") == 9606

  def test_parses_plain_integer_string(self):
    assert extract_taxon_id("9606") == 9606

  def test_parses_other_prefix(self):
    assert extract_taxon_id("taxon:10090") == 10090
