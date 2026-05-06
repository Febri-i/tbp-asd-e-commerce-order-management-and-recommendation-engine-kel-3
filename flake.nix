{
  description = "Python development environment with Matplotlib and PySerial";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      # Systems supported
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      # Helper function to generate attributes for each system
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};

          # Define the Python environment with specific packages
          pythonEnv = pkgs.python3.withPackages (
            ps: with ps; [
            ]
          );

        in
        {
          default = pkgs.mkShell {
            packages = [
              pythonEnv
            ];

            shellHook = ''
              echo "HELL YEAHHHHH"
            '';
          };
        }
      );
    };
}
