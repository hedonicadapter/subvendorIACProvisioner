let
  pkgs = import <nixpkgs> {config.allowUnfree = true;};

  python-env = pkgs.python311.withPackages (pp: with pp; [pip wheel cython]);
in
  pkgs.mkShell {
    packages = with pkgs;
      [
        vscode

        azure-cli
        azure-functions-core-tools

        bicep
        terraform
        powershell
      ]
      # Language servers
      ++ [
        terraform-ls
        terraform-lsp
      ]
      # Linters
      ++ [
      ];

    buildInputs = [
      python-env
    ];

    shellHook = ''
      [[ -d .venv ]] || python -m venv .venv
      source .venv/bin/activate
    '';
  }
