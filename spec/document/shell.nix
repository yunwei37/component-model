{ nixpkgs ? import <nixpkgs> {} }: with nixpkgs;
stdenv.mkDerivation {
  name = "wasm-components-spec";
  buildInputs = [ gnumake sphinx texlive.combined.scheme-full ];
}
