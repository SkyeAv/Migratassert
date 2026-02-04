"""Tests for source mapper."""

import pytest
from migratassert.source import map_source


class TestMapSource:
  def test_maps_url_and_local(self):
    v440 = {
      "where_to_download_data_from": "https://example.com/data.csv",
      "posix_filepath": "/data/cache/data.csv",
    }
    result = map_source(v440)
    assert result.mapped["url"] == "https://example.com/data.csv"
    assert result.mapped["local"] == "/data/cache/data.csv"

  def test_maps_excel_hyperparameters(self):
    v440 = {
      "posix_filepath": "/data/file.xlsx",
      "download_hyperparameters": {
        "file_extension": "xlsx",
        "which_excel_sheet_to_use": "Results",
        "start_at_line_number": 2,
        "end_at_line_number": 100,
      },
    }
    result = map_source(v440)
    assert result.mapped["kind"] == "excel"
    assert result.mapped["sheet"] == "Results"
    assert result.mapped["row_slice"] == [2, 100]

  def test_maps_text_hyperparameters(self):
    v440 = {
      "posix_filepath": "/data/file.tsv",
      "download_hyperparameters": {
        "file_extension": "tsv",
        "file_delimiter": "\t",
        "use_row_numbers": [1, 5, 10, 15],
      },
    }
    result = map_source(v440)
    assert result.mapped["kind"] == "text"
    assert result.mapped["delimiter"] == "\t"
    assert result.mapped["rows"] == [1, 5, 10, 15]

  def test_includes_reindexing(self):
    v440 = {"posix_filepath": "/data/file.csv"}
    reindexing = [
      {
        "when": "after",
        "column": "pvalue",
        "comparison": "lt",
        "value_for_comparison": 0.05,
      }
    ]
    result = map_source(v440, reindexing=reindexing)
    assert result.mapped["reindex"] == [
      {"column": "pvalue", "comparison": "lt", "comparator": 0.05}
    ]
