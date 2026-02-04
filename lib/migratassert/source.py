"""Map location block to source block."""

from typing import Any

from migratassert.encoding import MapResult

# File extension to kind mapping
EXTENSION_TO_KIND = {
  "xlsx": "excel",
  "xls": "excel",
  "csv": "text",
  "tsv": "text",
  "txt": "text",
}


def map_reindexing(
  filters: list[dict[str, Any]],
) -> list[dict[str, Any]]:
  """Map v4.4.0 reindexing filters to TC3 reindex format.

  Args:
    filters: List of filter dicts with when, column, comparison, value_for_comparison

  Returns:
    List of TC3 reindex dicts (drops 'when', renames value_for_comparison -> comparator)
  """
  return [
    {
      "column": f["column"],
      "comparison": f["comparison"],
      "comparator": f["value_for_comparison"],
    }
    for f in filters
    if "column" in f and "comparison" in f and "value_for_comparison" in f
  ]


def map_source(
  location: dict[str, Any],
  reindexing: list[dict[str, Any]] | None = None,
) -> MapResult:
  """Map v4.4.0 location block to TC3 source block.

  Args:
    location: Source location dict
    reindexing: Optional reindexing filters to include

  Returns:
    MapResult with TC3 source block
  """
  dropped: list[str] = []
  source: dict[str, Any] = {}

  if "where_to_download_data_from" in location:
    source["url"] = location["where_to_download_data_from"]

  if "posix_filepath" in location:
    source["local"] = location["posix_filepath"]

  hyper = location.get("download_hyperparameters", {})

  if "file_extension" in hyper:
    ext = hyper["file_extension"].lstrip(".")
    source["kind"] = EXTENSION_TO_KIND.get(ext, "text")

  if "file_delimiter" in hyper:
    source["delimiter"] = hyper["file_delimiter"]

  if "which_excel_sheet_to_use" in hyper:
    source["sheet"] = hyper["which_excel_sheet_to_use"]

  start = hyper.get("start_at_line_number")
  end = hyper.get("end_at_line_number")
  if start is not None or end is not None:
    source["row_slice"] = [start, end]

  if "use_row_numbers" in hyper:
    source["rows"] = hyper["use_row_numbers"]

  if reindexing:
    source["reindex"] = map_reindexing(reindexing)

  return MapResult(mapped=source, dropped=dropped)
