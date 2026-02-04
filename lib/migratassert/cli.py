"""Typer CLI entry point for migratassert."""

from pathlib import Path

import typer

from migratassert.migrate import run_migration
from migratassert.report import print_report

app = typer.Typer(
  name="migratassert",
  help="Migrate Tablassert YAML configs from v4.4.0 to TC3 schema",
  add_completion=False,
)


@app.command()
def migrate(
  input_dir: Path = typer.Argument(
    ...,
    help="Directory containing v4.4.0 YAML files",
    exists=True,
    file_okay=False,
    dir_okay=True,
    readable=True,
  ),
  output_dir: Path = typer.Argument(
    ...,
    help="Directory for migrated TC3 YAML files",
  ),
  dry_run: bool = typer.Option(
    False,
    "--dry-run",
    "-n",
    help="Show what would be migrated without writing files",
  ),
  verbose: bool = typer.Option(
    False,
    "--verbose",
    "-v",
    help="Show detailed migration info per file",
  ),
) -> None:
  """Migrate Tablassert YAML configs from v4.4.0 to TC3 schema."""
  if dry_run:
    typer.echo(
      f"DRY RUN: Would migrate files from {input_dir} to {output_dir}\n"
    )
  else:
    output_dir.mkdir(parents=True, exist_ok=True)

  result = run_migration(
    input_dir,
    output_dir,
    dry_run=dry_run,
  )

  print_report(result, verbose=verbose)

  if result.files_failed > 0:
    raise typer.Exit(code=1)


if __name__ == "__main__":
  app()
