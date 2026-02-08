{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    python3
    uv
    stdenv.cc.cc.lib  # provides libstdc++.so.6
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
    echo "Nix shell loaded - numpy can now find libstdc++.so.6"
  '';
}
