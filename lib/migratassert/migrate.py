"""Batch migration orchestration with 2-space YAML indentation."""

from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

from migratassert.transform import transform_config


@dataclass
class FileResult:
  """Result of migrating a single file."""

  source_path: Path
  dest_path: Path
  success: bool
  dropped_fields: list[str] = field(default_factory=list)
  error: str | None = None


@dataclass
class MigrationResult:
  """Aggregate result of batch migration."""

  files_processed: int = 0
  files_succeeded: int = 0
  files_failed: int = 0
  file_results: list[FileResult] = field(default_factory=list)
  all_dropped_fields: dict[str, int] = field(default_factory=dict)


def get_yaml() -> YAML:
  """Get configured YAML instance with 2-space indentation.

  Uses sequence=4 with offset=2 to ensure list item mappings
  align correctly (the `-` is indented 2, content is offset 2 more).
  """
  yaml = YAML()
  yaml.indent(mapping=2, sequence=4, offset=2)
  yaml.default_flow_style = False
  return yaml


def to_commented(data: Any, parent_key: str = "") -> Any:
  """Convert plain Python dicts/lists to ruamel.yaml CommentedMap/CommentedSeq.

  This ensures proper YAML indentation and flow style control.

  Args:
    data: Data structure to convert
    parent_key: Key path for context (used to determine flow style)

  Returns:
    Converted data with CommentedMap/CommentedSeq for proper formatting
  """
  if isinstance(data, dict):
    cm = CommentedMap()
    for k, v in data.items():
      cm[k] = to_commented(v, parent_key=k)
    return cm
  elif isinstance(data, list):
    cs = CommentedSeq()
    for item in data:
      cs.append(to_commented(item, parent_key=parent_key))
    return cs
  return data


def dump_yaml(data: dict[str, Any]) -> str:
  """Dump data to YAML string with 2-space indentation.

  Args:
    data: Dictionary to dump

  Returns:
    YAML string with 2-space indentation
  """
  yaml = get_yaml()
  stream = StringIO()
  yaml.dump(to_commented(data), stream)
  return stream.getvalue()


def discover_yaml_files(indir: Path) -> list[Path]:
  """Find all YAML files in directory (non-recursive).

  Args:
    indir: Directory to search

  Returns:
    List of YAML file paths sorted by name
  """
  yaml_files = list(indir.glob("*.yaml")) + list(indir.glob("*.yml"))
  return sorted(yaml_files, key=lambda p: p.name)


def migrate_file(
  source_path: Path,
  dest_path: Path,
  dry_run: bool = False,
) -> FileResult:
  """Migrate a single YAML file.

  Args:
    source_path: Path to v4.4.0 YAML file
    dest_path: Path for output TC3 YAML file
    dry_run: If True, don't write output file

  Returns:
    FileResult with migration details
  """
  yaml = get_yaml()

  try:
    with open(source_path) as f:
      v440_config = yaml.load(f)

    result = transform_config(v440_config)

    if not dry_run:
      dest_path.parent.mkdir(parents=True, exist_ok=True)
      with open(dest_path, "w") as f:
        yaml.dump(to_commented(result.config), f)

    return FileResult(
      source_path=source_path,
      dest_path=dest_path,
      success=True,
      dropped_fields=result.dropped_fields,
    )

  except Exception as e:
    return FileResult(
      source_path=source_path,
      dest_path=dest_path,
      success=False,
      error=str(e),
    )


def run_migration(
  indir: Path,
  outdir: Path,
  dry_run: bool = False,
) -> MigrationResult:
  """Run batch migration on all YAML files in directory.

  Args:
    indir: Directory containing v4.4.0 files
    outdir: Directory for TC3 output files
    dry_run: If True, don't write files

  Returns:
    MigrationResult with aggregate statistics
  """
  result = MigrationResult()
  yaml_files = discover_yaml_files(indir)

  for source_path in yaml_files:
    dest_path = outdir / source_path.name
    file_result = migrate_file(source_path, dest_path, dry_run=dry_run)

    result.files_processed += 1
    result.file_results.append(file_result)

    if file_result.success:
      result.files_succeeded += 1
      for field_name in file_result.dropped_fields:
        result.all_dropped_fields[field_name] = (
          result.all_dropped_fields.get(field_name, 0) + 1
        )
    else:
      result.files_failed += 1

  return result
