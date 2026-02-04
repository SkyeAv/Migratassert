final: prev: {
  python313Packages = prev.python313Packages.override {
    overrides = pyFinal: pyPrev: {
      migratassert = pyFinal.buildPythonApplication rec {
        pname = "migratassert";
        version = "0.1.0";
        format = "pyproject";
        src = ../.;
        build-system = with pyFinal; [
          setuptools
          wheel
        ];
        propagatedBuildInputs = with pyFinal; [
          ruamel.yaml
          typer
        ];
        doCheck = false;
      };
    };
  };
}
