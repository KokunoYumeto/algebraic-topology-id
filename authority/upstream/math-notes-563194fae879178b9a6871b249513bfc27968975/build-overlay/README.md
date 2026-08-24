# Fomberg baseline build overlay

The frozen SourceHut witness is never edited. `commath.sty` is a minimal,
independently authored compatibility layer used only at build time because the
current local TeX installation does not provide the upstream header's
`commath.sty` dependency.

The complete `algebraic_topology.tex` source uses only `\set`, `\del`,
`\norm`, and `\abs` from that package; `header.tex` additionally expects
`\dif` and `\Dif` to exist before it renews them. The overlay implements only
those six conventional mathematical delimiters/operators. It preserves the
optional manual delimiter sizes used by the frozen source (`\del[1]` once and
`\del[4]` three times); no other optional form occurs. It contains no code
copied from the `commath` package and is dedicated to the public domain under
CC0 1.0 (`SPDX-License-Identifier: CC0-1.0`).

`scripts/build-fomberg-authority-baseline.ps1` places this directory first on
`TEXINPUTS`, copies the exact frozen source and header into two independent
clean build directories, and compares the resulting PDFs byte for byte. In the
disposable header copies only, it also omits four package loads that the complete
`algebraic_topology.tex` source never uses: `esvect`, `esdiff`, `witharrows`, and
`quiver`. The exact frozen `header.tex` remains unchanged. The full 57-page
source compiles with package installation disabled, and the visual comparison
against the official PDF confirms that the omissions are semantically inert.
