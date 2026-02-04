"""Map attributes block to annotations block."""

from typing import Any

from migratassert.encoding import MapResult, map_node_encoding


def map_annotations(attributes: dict[str, Any]) -> MapResult:
  """Map v4.4.0 attributes to TC3 annotations.

  Args:
    attributes: Source attributes dict (keys are attribute names,
      values are encoding dicts)

  Returns:
    MapResult with TC3 annotations block
  """
  dropped: list[str] = []
  annotations: dict[str, Any] = {}

  for attr_name, attr_value in attributes.items():
    if isinstance(attr_value, dict):
      enc_result = map_node_encoding(
        attr_value,
        field_prefix=f"attributes.{attr_name}.",
      )
      annotations[attr_name] = enc_result.mapped
      dropped.extend(enc_result.dropped)
    else:
      annotations[attr_name] = attr_value

  return MapResult(mapped=annotations, dropped=dropped)
