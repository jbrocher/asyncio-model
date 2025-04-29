{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = {
    self,
    nixpkgs,
    poetry2nix,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (poetry2nix.lib.mkPoetry2Nix {pkgs = pkgs.${system};}) mkPoetryApplication;
    in {
      packages = {
        default = mkPoetryApplication {projectDir = self;};
      };
      devShells = let
        inherit (poetry2nix.lib.mkPoetry2Nix {pkgs = pkgs;}) mkPoetryEnv defaultPoetryOverrides;
        python = pkgs.python312;
        # lib = pkgs.lib;
        pypkgs-build-requirements = {
          # pandas = ["versioneer"];
        };
        env = mkPoetryEnv {
          projectDir = self;
          python = python;
          preferWheels = true;
          overrides = defaultPoetryOverrides.extend (self: super:
            builtins.mapAttrs (
              package: build-requirements:
                (builtins.getAttr package super).overridePythonAttrs (old: {
                  buildInputs =
                    (old.buildInputs or [])
                    ++ (builtins.map (pkg:
                      if builtins.isString pkg
                      then builtins.getAttr pkg super
                      else pkg)
                    build-requirements);
                })
            )
            pypkgs-build-requirements);
        };
      in {
        default = env.env.overrideAttrs (old: {
          buildInputs = [(pkgs.poetry.overrideAttrs {python = python;})];
          # NIX_LD_LIBRARY_PATH =
          #   lib.makeLibraryPath [
          #   ];
          # NIX_LD = lib.fileContents "${pkgs.stdenv.cc}/nix-support/dynamic-linker";
        });
      };
    });
}
