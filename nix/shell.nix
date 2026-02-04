{pkgs, lib, config, ...}:
let
  py = pkgs.python313Packages;
in {
  packages.default = py.migratassert;
  devShells.default = pkgs.mkShell {
    packages = with py; [
      migratassert
      pytest-cov
      pytest
    ];
  };
}
