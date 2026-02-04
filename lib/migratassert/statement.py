"""Map triple block to statement block."""

from typing import Any

from migratassert.encoding import MapResult, map_node_encoding


def map_statement(triple: dict[str, Any]) -> MapResult:
  """Map v4.4.0 triple block to TC3 statement block.

  Args:
    triple: Source triple dict with triple_subject, triple_predicate, triple_object

  Returns:
    MapResult with TC3 statement block
  """
  dropped: list[str] = []
  statement: dict[str, Any] = {}

  if "triple_subject" in triple:
    subj_result = map_node_encoding(
      triple["triple_subject"],
      field_prefix="triple.subject.",
    )
    statement["subject"] = subj_result.mapped
    dropped.extend(subj_result.dropped)

  if "triple_predicate" in triple:
    pred = triple["triple_predicate"]
    if isinstance(pred, dict):
      statement["predicate"] = pred.get("value_for_encoding", "")
    else:
      statement["predicate"] = pred

  if "triple_object" in triple:
    obj_result = map_node_encoding(
      triple["triple_object"],
      field_prefix="triple.object.",
    )
    statement["object"] = obj_result.mapped
    dropped.extend(obj_result.dropped)

  return MapResult(mapped=statement, dropped=dropped)
