"""Map provenance block to TC3 format."""

from typing import Any

from migratassert.encoding import MapResult

# Known publication CURIE prefixes
PUBLICATION_REPOS = {"PMC", "PMID", "DOI"}


def parse_publication_curie(curie: str) -> tuple[str, str]:
  """Parse publication CURIE into repo and ID.

  Args:
    curie: CURIE like 'PMC:123456' or 'DOI:10.1234/foo'

  Returns:
    Tuple of (repo, publication_id)
  """
  if ":" not in curie:
    return ("", curie)
  repo, pub_id = curie.split(":", 1)
  return (repo.upper(), pub_id)


def map_provenance(provenance: dict[str, Any]) -> MapResult:
  """Map v4.4.0 provenance to TC3 provenance.

  Args:
    provenance: Source provenance dict with publication,
      config_curator_name, config_curator_organization

  Returns:
    MapResult with TC3 provenance block
  """
  dropped: list[str] = []
  tc3_prov: dict[str, Any] = {}

  if "publication" in provenance:
    repo, pub_id = parse_publication_curie(provenance["publication"])
    if repo in PUBLICATION_REPOS:
      tc3_prov["repo"] = repo
    tc3_prov["publication"] = pub_id

  if "config_curator_name" in provenance:
    contributor: dict[str, Any] = {
      "kind": "curation",
      "name": provenance["config_curator_name"],
    }
    if "config_curator_organization" in provenance:
      contributor["organizations"] = [provenance["config_curator_organization"]]
    tc3_prov["contributors"] = [contributor]

  return MapResult(mapped=tc3_prov, dropped=dropped)
