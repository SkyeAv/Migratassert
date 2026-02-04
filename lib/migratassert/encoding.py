"""NodeEncoding transformation (shared by statement and annotations)."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MapResult:
  """Result of a mapping operation."""

  mapped: dict[str, Any]
  dropped: list[str] = field(default_factory=list)


def extract_taxon_id(curie: str) -> int:
  """Extract integer taxon ID from CURIE like 'NCBITaxon:9606'.

  Args:
    curie: CURIE string (e.g., 'NCBITaxon:9606') or plain integer string

  Returns:
    Integer taxon ID
  """
  if ":" in curie:
    _, taxon_str = curie.rsplit(":", 1)
    return int(taxon_str)
  return int(curie)


def map_transformations(
  math_module: dict[str, Any] | list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
  """Map math_module_transformations to transformations array.

  Args:
    math_module: Source math_module_transformations (single dict or list)

  Returns:
    List of transformation dicts with 'function' and 'arguments'
  """
  if math_module is None:
    return []

  if isinstance(math_module, dict):
    transforms = [math_module]
  else:
    transforms = math_module

  return [
    {
      "function": t.get("attribute"),
      "arguments": t.get("arguments"),
    }
    for t in transforms
    if t.get("attribute")
  ]
