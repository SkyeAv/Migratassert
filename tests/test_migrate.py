"""Tests for migration orchestration."""

import pytest
from pathlib import Path

from migratassert.migrate import (
  discover_yaml_files,
  migrate_file,
  run_migration,
  dump_yaml,
)


@pytest.fixture
def sample_v440_config():
  return {
    "template": {
      "location": {"posix_filepath": "/data/test.csv"},
      "triple": {
        "triple_subject": {"encoding_method": "column", "value_for_encoding": "A"},
        "triple_predicate": {"value_for_encoding": "biolink:related_to"},
        "triple_object": {"encoding_method": "column", "value_for_encoding": "B"},
      },
    }
  }


class TestDumpYaml:
  def test_uses_two_space_indentation(self):
    data = {"template": {"source": {"kind": "text"}}}
    output = dump_yaml(data)
    assert "  source:" in output
    assert "    kind:" in output
    assert "      " not in output.replace("    kind:", "")


class TestDiscoverYamlFiles:
  def test_finds_yaml_files(self, tmp_path):
    (tmp_path / "config1.yaml").touch()
    (tmp_path / "config2.yml").touch()
    (tmp_path / "other.txt").touch()
    files = discover_yaml_files(tmp_path)
    assert len(files) == 2
    assert all(f.suffix in (".yaml", ".yml") for f in files)


class TestMigrateFile:
  def test_transforms_file(self, tmp_path, sample_v440_config):
    from ruamel.yaml import YAML
    yaml = YAML()

    source = tmp_path / "input.yaml"
    dest = tmp_path / "output.yaml"

    with open(source, "w") as f:
      yaml.dump(sample_v440_config, f)

    result = migrate_file(source, dest)
    assert result.success
    assert dest.exists()

    with open(dest) as f:
      content = f.read()
    assert "syntax: TC3" in content
    assert "  source:" in content or "  statement:" in content

  def test_dry_run_does_not_write(self, tmp_path, sample_v440_config):
    from ruamel.yaml import YAML
    yaml = YAML()

    source = tmp_path / "input.yaml"
    dest = tmp_path / "output.yaml"

    with open(source, "w") as f:
      yaml.dump(sample_v440_config, f)

    result = migrate_file(source, dest, dry_run=True)
    assert result.success
    assert not dest.exists()


class TestRunMigration:
  def test_processes_directory(self, tmp_path, sample_v440_config):
    from ruamel.yaml import YAML
    yaml = YAML()

    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    for i in range(3):
      with open(input_dir / f"config{i}.yaml", "w") as f:
        yaml.dump(sample_v440_config, f)

    result = run_migration(input_dir, output_dir)
    assert result.files_processed == 3
    assert result.files_succeeded == 3
    assert len(list(output_dir.glob("*.yaml"))) == 3
