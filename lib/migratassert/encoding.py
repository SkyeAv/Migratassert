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


# Field rename mapping for NodeEncoding
ENCODING_FIELD_MAP = {
  "encoding_method": "method",
  "value_for_encoding": "encoding",
}

HYPERPARAMETER_FIELD_MAP = {
  "in_this_organism": "taxon",
  "classes_to_prioritize": "prioritize",
  "classes_to_avoid": "avoid",
  "prefix": "prefix",
  "suffix": "suffix",
  "substrings_to_remove": "remove",
  "regular_expressions": "regex",
  "explode_by_delimiter": "explode_by",
}

# Fields to silently drop (no TC3 equivalent)
DROPPED_FIELDS = {"how_to_fill_column"}


def map_node_encoding(
  v440_encoding: dict[str, Any],
  field_prefix: str = "",
) -> MapResult:
  """Map v4.4.0 encoding fields to TC3 NodeEncoding.

  Args:
    v440_encoding: Source encoding dict with encoding_method,
      value_for_encoding, mapping_hyperparameters, etc.
    field_prefix: Prefix for dropped field names (e.g., "subject.")

  Returns:
    MapResult with mapped TC3 NodeEncoding and dropped field names
  """
  dropped: list[str] = []
  tc3: dict[str, Any] = {}

  for old_key, new_key in ENCODING_FIELD_MAP.items():
    if old_key in v440_encoding:
      tc3[new_key] = v440_encoding[old_key]

  hyper = v440_encoding.get("mapping_hyperparameters", {})
  for old_key, new_key in HYPERPARAMETER_FIELD_MAP.items():
    if old_key in hyper:
      value = hyper[old_key]
      if new_key == "taxon" and isinstance(value, str):
        value = extract_taxon_id(value)
      tc3[new_key] = value

  known_hyper_fields = set(HYPERPARAMETER_FIELD_MAP.keys()) | DROPPED_FIELDS
  for key in hyper:
    if key not in known_hyper_fields:
      dropped.append(f"{field_prefix}{key}")
    elif key in DROPPED_FIELDS:
      dropped.append(f"{field_prefix}{key}")

  if "math_module_transformations" in v440_encoding:
    transforms = map_transformations(v440_encoding["math_module_transformations"])
    if transforms:
      tc3["transformations"] = transforms

  return MapResult(mapped=tc3, dropped=dropped)
