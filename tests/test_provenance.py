"""Tests for provenance mapper."""

import pytest
from migratassert.provenance import map_provenance, parse_publication_curie


class TestParsePublicationCurie:
  def test_parses_pmc(self):
    assert parse_publication_curie("PMC:11708054") == ("PMC", "11708054")

  def test_parses_pmid(self):
    assert parse_publication_curie("PMID:12345678") == ("PMID", "12345678")

  def test_parses_doi(self):
    assert parse_publication_curie("DOI:10.1234/example") == ("DOI", "10.1234/example")

  def test_handles_no_prefix(self):
    assert parse_publication_curie("11708054") == ("", "11708054")


class TestMapProvenance:
  def test_maps_publication_curie(self):
    v440 = {"publication": "PMC:11708054"}
    result = map_provenance(v440)
    assert result.mapped["repo"] == "PMC"
    assert result.mapped["publication"] == "11708054"

  def test_maps_curator_to_contributors(self):
    v440 = {
      "publication": "PMID:12345",
      "config_curator_name": "Jane Doe",
      "config_curator_organization": "Example University",
    }
    result = map_provenance(v440)
    assert len(result.mapped["contributors"]) == 1
    contrib = result.mapped["contributors"][0]
    assert contrib["kind"] == "curation"
    assert contrib["name"] == "Jane Doe"
    assert contrib["organizations"] == ["Example University"]

  def test_curator_without_organization(self):
    v440 = {
      "publication": "DOI:10.1234/foo",
      "config_curator_name": "John Smith",
    }
    result = map_provenance(v440)
    contrib = result.mapped["contributors"][0]
    assert contrib["name"] == "John Smith"
    assert "organizations" not in contrib
