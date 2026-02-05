# Tablassert YAML Migration Tool

Migrate Tablassert configuration YAML files from v4.4.0 schema to TC3 schema.

## Quick Start

```bash
# Clone repository
git clone https://github.com/SkyeAv/MIGRATIONS.git
cd MIGRATIONS

# Enter development shell
nix develop -L .

# Run CLI
migratassert-cli --help
```

## Usage (With Nix)

### Method 1: Development Shell (Recommended)

Best for exploring MIGRATIONS or active development.

```bash
# Clone and enter development shell
git clone https://github.com/SkyeAv/Migratassert.git
cd MIGRATIONS
nix develop -L .

# CLI is now available
migratassert-cli -i ./v440_configs/ -o ./tc3_configs/
```

### Method 2: Direct Run from Flake

Run without cloning or installing.

```bash
nix run github:SkyeAv/Migratassert#default -- -i ./v440_configs/ -o ./tc3_configs/
```

### Method 3: User Profile Installation

Install persistently to your user environment.

```bash
# Install
nix profile install github:SkyeAv/Migratassert#default

# Use anywhere
migratassert-cli -i ./v440_configs/ -o ./tc3_configs/
```

### Method 4: Use as Overlay

Integrate into your own Nix flake or NixOS configuration.

```nix
{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    migratassert.url = "github:SkyeAv/MIGRATIONS";
  };

  outputs = { self, nixpkgs, migratassert }: {
    # Add overlay to nixpkgs
    pkgs = import nixpkgs {
      system = "x86_64-linux";
      overlays = [ migratassert.overlays.default ];
    };

    # Migratassert available as pkgs.python313Packages.migratassert
    devShells.default = pkgs.mkShell {
      packages = [ pkgs.python313Packages.migratassert ];
    };
  };
}
```

## CLI Usage

### Basic Migration

```bash
migratassert-cli -i ./v440_configs/ -o ./tc3_configs/
```

### Dry Run (Preview)

```bash
migratassert-cli -i ./v440_configs/ -o ./tc3_configs/ --dry-run
```

### Verbose Output

```bash
migratassert-cli -i ./v440_configs/ -o ./tc3_configs/ --verbose
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
| `how_to_fill_column` | `fill` |

### New Fields

- `syntax: TC3` added at template root

### Dropped Fields

- `when` (reindexing) - no TC3 equivalent

## Development

Run tests:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=migratassert --cov-report=term-missing
```
