"""Migration report generation."""

from migratassert.migrate import MigrationResult


def format_report(result: MigrationResult) -> str:
  """Format migration result as human-readable report.

  Args:
    result: MigrationResult from batch migration

  Returns:
    Formatted report string
  """
  lines = [
    "=" * 60,
    "TABLASSERT MIGRATION REPORT (v4.4.0 -> TC3)",
    "=" * 60,
    "",
    f"Files processed: {result.files_processed}",
    f"  Succeeded: {result.files_succeeded}",
    f"  Failed: {result.files_failed}",
    "",
  ]

  if result.all_dropped_fields:
    lines.append("Dropped fields (across all files):")
    for field_name, count in sorted(
      result.all_dropped_fields.items(),
      key=lambda x: (-x[1], x[0]),
    ):
      lines.append(f"  {field_name}: {count} occurrences")
    lines.append("")

  if result.files_failed > 0:
    lines.append("Failed files:")
    for fr in result.file_results:
      if not fr.success:
        lines.append(f"  {fr.source_path.name}: {fr.error}")
    lines.append("")

  lines.append("=" * 60)
  return "\n".join(lines)


def print_report(result: MigrationResult, verbose: bool = False) -> None:
  """Print migration report to stdout.

  Args:
    result: MigrationResult from batch migration
    verbose: If True, show per-file details
  """
  print(format_report(result))

  if verbose and result.file_results:
    print("\nPer-file details:")
    for fr in result.file_results:
      status = "OK" if fr.success else "FAILED"
      print(f"  [{status}] {fr.source_path.name}")
      if fr.dropped_fields:
        for field_name in fr.dropped_fields:
          print(f"         dropped: {field_name}")
