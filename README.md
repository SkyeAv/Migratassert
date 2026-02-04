# Tablassert YAML Migration Tool

Migrate Tablassert configuration YAML files from v4.4.0 schema to TC3 schema.

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Usage

### Basic Migration

```bash
migratassert ./v440_configs/ ./tc3_configs/
```

### Dry Run (Preview)

```bash
migratassert --dry-run ./v440_configs/ ./tc3_configs/
```

### Verbose Output

```bash
migratassert -v ./v440_configs/ ./tc3_configs/
```

## Output Format

- **2-space indentation** (matching Tablassert conventions)
- Clean YAML without flow style

## Schema Changes

### Block Renames

| v4.4.0 | TC3 |
|--------|-----|
| `location` | `source` |
| `triple` | `statement` |
| `attributes` | `annotations` |
| `reindexing` | `source.reindex` |

### Field Renames

| v4.4.0 | TC3 |
|--------|-----|
| `encoding_method` | `method` |
| `value_for_encoding` | `encoding` |
| `in_this_organism` | `taxon` (integer) |
| `classes_to_prioritize` | `prioritize` |
| `classes_to_avoid` | `avoid` |
| `substrings_to_remove` | `remove` |
| `regular_expressions` | `regex` |
| `explode_by_delimiter` | `explode_by` |
| `value_for_comparison` | `comparator` |

### New Fields

- `syntax: TC3` added at template root

### Dropped Fields

- `when` (reindexing) - no TC3 equivalent
- `how_to_fill_column` - no TC3 equivalent

## Development

Run tests:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=migratassert --cov-report=term-missing
```
