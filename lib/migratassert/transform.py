"""Core transformation logic for v4.4.0 -> TC3."""

from dataclasses import dataclass, field
from typing import Any

from migratassert.annotations import map_annotations
from migratassert.provenance import map_provenance
from migratassert.source import map_source
from migratassert.statement import map_statement


@dataclass
class TransformResult:
  """Result of transforming a single config."""

  config: dict[str, Any]
  dropped_fields: list[str] = field(default_factory=list)


def transform_config(v440_config: dict[str, Any], file_stem: str | None = None) -> TransformResult:
  """Transform a v4.4.0 config to TC3 schema.

  Args:
    v440_config: Parsed v4.4.0 YAML config
    file_stem: Optional file stem for default local field generation

  Returns:
    TransformResult with TC3 config and list of dropped fields
  """
  dropped: list[str] = []
  template = v440_config.get("template", {})

  tc3_template: dict[str, Any] = {"syntax": "TC3"}

  if "location" in template:
    source_result = map_source(
      template["location"],
      reindexing=template.get("reindexing"),
      file_stem=file_stem,
    )
    tc3_template["source"] = source_result.mapped
    dropped.extend(source_result.dropped)

  if "triple" in template:
    stmt_result = map_statement(template["triple"])
    tc3_template["statement"] = stmt_result.mapped
    dropped.extend(stmt_result.dropped)

  if "provenance" in template:
    prov_result = map_provenance(template["provenance"])
    tc3_template["provenance"] = prov_result.mapped
    dropped.extend(prov_result.dropped)

  if "attributes" in template:
    annot_result = map_annotations(template["attributes"])
    tc3_template["annotations"] = annot_result.mapped
    dropped.extend(annot_result.dropped)

  if "sections" in template:
    tc3_sections: list[dict[str, Any]] = []
    for section in template["sections"]:
      tc3_section: dict[str, Any] = {}

      if "location" in section:
        source_result = map_source(
          section["location"],
          reindexing=section.get("reindexing"),
          file_stem=file_stem,
        )
        tc3_section["source"] = source_result.mapped
        dropped.extend(source_result.dropped)

      if "triple" in section:
        stmt_result = map_statement(section["triple"])
        tc3_section["statement"] = stmt_result.mapped
        dropped.extend(stmt_result.dropped)

      if "provenance" in section:
        prov_result = map_provenance(section["provenance"])
        tc3_section["provenance"] = prov_result.mapped
        dropped.extend(prov_result.dropped)

      if "attributes" in section:
        annot_result = map_annotations(section["attributes"])
        tc3_section["annotations"] = annot_result.mapped
        dropped.extend(annot_result.dropped)

      keys_requiring_transformation = {"location", "triple", "provenance", "attributes", "reindexing"}
      for key, value in section.items():
        if key not in keys_requiring_transformation:
          tc3_section[key] = value

      tc3_sections.append(tc3_section)

    tc3_template["sections"] = tc3_sections

  return TransformResult(
    config={"template": tc3_template},
    dropped_fields=dropped,
  )
