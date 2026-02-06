"""Map attributes block to annotations block."""

from typing import Any

from migratassert.encoding import MapResult, map_node_encoding


# Common attribute name mappings (underscore to human-readable)
ANNOTATION_NAME_MAP = {
  "p_value": "p value",
  "sample_size": "sample size",
  "multiple_testing_correction_method": "multiple testing correction method",
  "relationship_strength": "relationship strength",
  "assertion_method": "assertion method",
  "notes": "miscellaneous notes",
}


def normalize_annotation_name(name: str) -> str:
  """Convert attribute name to TC3 annotation name.

  Args:
    name: Attribute name (may have underscores)

  Returns:
    Human-readable annotation name (spaces instead of underscores)
  """
  # Check for known mappings first
  if name in ANNOTATION_NAME_MAP:
    return ANNOTATION_NAME_MAP[name]
  # Default: replace underscores with spaces
  return name.replace("_", " ")


def map_annotations(attributes: dict[str, Any]) -> MapResult:
  """Map v4.4.0 attributes to TC3 annotations.

  TC3 expects annotations as a list of objects, each with an
  'annotation' key for the name.

  Args:
    attributes: Source attributes dict (keys are attribute names,
      values are encoding dicts or plain values)

  Returns:
    MapResult with TC3 annotations list
  """
  dropped: list[str] = []
  annotations: list[dict[str, Any]] = []

  for attr_name, attr_value in attributes.items():
    annotation_name = normalize_annotation_name(attr_name)

    if isinstance(attr_value, dict):
      enc_result = map_node_encoding(
        attr_value,
        field_prefix=f"attributes.{attr_name}.",
      )
      # Build annotation object with 'annotation' key first
      annotation_obj: dict[str, Any] = {"annotation": annotation_name}
      annotation_obj.update(enc_result.mapped)
      annotations.append(annotation_obj)
      dropped.extend(enc_result.dropped)
    else:
      # Plain value (like notes string) becomes method: value
      annotations.append({
        "annotation": annotation_name,
        "method": "value",
        "encoding": attr_value,
      })

  return MapResult(mapped=annotations, dropped=dropped)
