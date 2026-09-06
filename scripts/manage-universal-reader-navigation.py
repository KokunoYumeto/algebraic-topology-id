#!/usr/bin/env python3
"""Apply or verify the D60 federated-reader navigation fragment.

The fragment is deliberately self-contained so every cumulative HTML reader
remains usable when downloaded. Verification removes the exact fragment in
memory and proves that the remaining bytes equal the previously published,
frozen reader bytes.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML_ROOT = ROOT / "output" / "html"
START = b"<!-- program-matematika-global-nav:start -->"
END = b"<!-- program-matematika-global-nav:end -->"

NAV_FRAGMENT = b'''\n<!-- program-matematika-global-nav:start -->
<style id="program-matematika-global-nav-style">
.program-matematika-global-nav{box-sizing:border-box;width:100%;margin:0 0 1.5rem;padding:.8rem 1rem;background:#102a43;color:#fff;border:2px solid #65d6ad;border-radius:.5rem;font:600 1rem/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}.program-matematika-global-nav__links{display:flex;flex-wrap:wrap;gap:.55rem 1rem;align-items:center}.program-matematika-global-nav a{color:#fff;text-decoration:underline;text-decoration-thickness:.12em;text-underline-offset:.18em}.program-matematika-global-nav a:focus-visible{outline:3px solid #ffd166;outline-offset:3px}.program-matematika-global-nav__label{font-weight:800}@media(prefers-color-scheme:dark){.program-matematika-global-nav{background:#071a2b;border-color:#7ce7c4}}
</style>
<nav class="program-matematika-global-nav" aria-label="Navigasi program matematika / Mathematics program navigation">
  <div class="program-matematika-global-nav__links">
    <span class="program-matematika-global-nav__label">D60 - Topologi Aljabar / Algebraic Topology</span>
    <a href="https://kokunoyumeto.github.io/program-matematika-indonesia/id/#course-D60">Program Bahasa Indonesia</a>
    <a href="https://kokunoyumeto.github.io/program-matematika-indonesia/en/#course-D60" lang="en">English program</a>
    <a href="https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/raw/master/Notes.pdf" lang="en">Sumber asli / Original: Roberts</a>
    <a href="https://yp.srht.site/notes/math/algebraic_topology.pdf" lang="en">Sumber asli / Original: Fomberg</a>
  </div>
</nav>
<!-- program-matematika-global-nav:end -->'''

# Exact pre-navigation identities from the previously deployed Pages workflow.
BASELINE = {
    "index.html": (85580, "5cc4a29f2c29b274328b574d6698a51d75af0939f9959937db8d679c38ad51b8"),
    "units-001-002/index.html": (220035, "d3b5cbfaa3511823821ecf9ba26a4eaec7c84d937417927d11bde3f66abc9f54"),
    "units-001-003/index.html": (359397, "33281cc46faa3d560c968b657526cd914786c991d1475b5563911a265bd316c1"),
    "units-001-004/index.html": (494732, "8c8f5e1ad8172a2d97e3931fc3b4f2a3aa7f9e8a709260a27103f7eca0f1357d"),
    "units-001-005/index.html": (610594, "8d3accf480101565409909c05f987f44b73f1c98889128e2f5074a4e049f48f3"),
    "units-001-007/index.html": (899803, "55135048eafe0f097c45936add885e008392eefdf475270fea37adf6a2a7b7bb"),
    "units-001-010/index.html": (1318415, "e228ac1422b2742d873feffd5b236fe9c1329d0bdb5da0e8deffe5e770361088"),
    "units-001-013/index.html": (1824804, "be1473ab5cb8eff26341e554179661775a12cec5784a8ebf3f9c2f3f0633cb71"),
    "units-001-019/index.html": (2962478, "ea5481b14dc1772408bd1c3e384b94a18eed9f2be3c9b9379fe4f8dd499253e0"),
    "units-001-020/index.html": (3190086, "59cb765f2291fc835ca629c774505303745983baacf5379efc97c49da6205c03"),
    "units-001-021/index.html": (3306661, "aec7e94d3697a7feeae87134da983c59faaf29dc8d961bca28b6bfa9c53cdfa6"),
    "units-001-022/index.html": (3520527, "15938aac7515e4ad7de66f8cf2d825744f9eb08b654165b835bfeace31aef8f4"),
    "units-001-023/index.html": (3707037, "536fbe19e295424d12198bf1b221be3e2f0170f87fa810a9125bcca9f742264b"),
    "units-001-024/index.html": (3927104, "28a84406de9e196070965920a7f7937177197977f9ddf118f0f8b07d464cbf0f"),
    "units-001-025/index.html": (4112563, "38cd8437f3b4235ac6269f4e3365123fa06485269d35a424ad4f5ddd589025c1"),
    "units-001-026/index.html": (4306392, "a9e4bea73cab5e90136822fbb94a11a1006f7e81ffcdf0a5740da52e335b4e3b"),
    "units-001-027/index.html": (4504569, "d98c2c29344e1e3cc3e81863e426fbf775ca6b70c0a5534d888d80ad2269486d"),
    "units-001-028/index.html": (4624723, "30f4821960a310bfb6f457f05838b6d8355e2a6df5c35b3a3dcdd9c1afa0a13e"),
    "units-001-029/index.html": (4751974, "67e5dd915cbbdf9b1961368efb1538b9ce0da8a4596d7ade11a4af051a189167"),
    "units-001-030/index.html": (4861791, "ed9da5653b3eacf7418d6e08760fcd2ecff4d75799c47f08689b940798099891"),
    "roberts-001-030-fomberg-001/index.html": (5029788, "2b64e8bec1dd5e1689ef6569360fec896ef87a683c7ba291a3780e27084a7390"),
    "roberts-001-030-fomberg-001-002/index.html": (5254038, "1f7618003e3ff273a4f1e2d97b5a81fd320f76640c475cae845ed38793fbeccd"),
    "roberts-001-030-fomberg-001-003/index.html": (7190228, "484a2a501df79b1810567810d0b454a18298a4cb43ef466c4e082622216b9542"),
    "roberts-001-030-fomberg-001-004/index.html": (8155605, "cd620d5557ff05fb81fb9cf044e8bd4848a6f92ef8fcd06078b8a124f6e79326"),
    "roberts-001-030-fomberg-001-005/index.html": (8353769, "d726c8d8a565172fb620233080f60e2ccbde4386d6fa03b099bf6219645aea90"),
    "roberts-001-030-fomberg-001-006/index.html": (12555960, "80a7d092cb786e4d4f7ecab31ba40746cf59398db50f0adca50f2431746f7c92"),
    "roberts-001-030-fomberg-001-007/index.html": (14885069, "87d58a5955954125c424ab1220a9c6aa7967a782a9bd739094a31ae0a50af5f6"),
    "roberts-001-030-fomberg-001-007-ca01/index.html": (14958219, "d71e2f3c0eb38b48fe4686a955ad555db3a407df8f18e41371d52908f0bdbbdf"),
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06/index.html": (15026881, "7ed278d73a324ba0a9e5acadedf448221b3791db7322fdf6d29225afd0124d2b"),
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03/index.html": (15287428, "417e50656ae0a61134c480f59df1bcd54d66a68c938d1d54f9c931ba37e2a5d6"),
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01/index.html": (15389821, "bb0cf484271370878508a6b774e442ee57aaf82b1a3bbca1bed086729360f7ff"),
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02/index.html": (15615104, "d0c6afddfa92759d475258bf08f20ea4019eccf72b7554128b2b938bd247b375"),
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03/index.html": (15828588, "c221955503cec820c7581c740a038ac1774999ac6a6014f8d0783da2cd08bf0d"),
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04/index.html": (15974648, "a76e31fc92e1554a6b14ffaccc1ad1001ee5c2838a3e36d1441b98519b39d4f8"),
    "roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04-capstone/index.html": (16049720, "a17ce8e3e4d6b93de5e678ce38f3b7834c3b6a9ca1bff063fd3e879875e254a8"),
}

REQUIRED_URLS = (
    b"https://kokunoyumeto.github.io/program-matematika-indonesia/id/#course-D60",
    b"https://kokunoyumeto.github.io/program-matematika-indonesia/en/#course-D60",
    b"https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/raw/master/Notes.pdf",
    b"https://yp.srht.site/notes/math/algebraic_topology.pdf",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strip_fragment(data: bytes) -> bytes:
    if data.count(START) != 1 or data.count(END) != 1:
        raise ValueError("navigation markers must occur exactly once")
    if data.count(NAV_FRAGMENT) != 1:
        raise ValueError("navigation fragment differs from the canonical bytes")
    return data.replace(NAV_FRAGMENT, b"", 1)


def verify_baseline(relative: str, data: bytes) -> None:
    expected_size, expected_sha = BASELINE[relative]
    if len(data) != expected_size:
        raise ValueError(f"{relative}: baseline size {len(data)} != {expected_size}")
    actual_sha = digest(data)
    if actual_sha != expected_sha:
        raise ValueError(f"{relative}: baseline SHA-256 {actual_sha} != {expected_sha}")


def apply() -> None:
    actual = sorted(p.relative_to(HTML_ROOT).as_posix() for p in HTML_ROOT.rglob("*.html"))
    if actual != sorted(BASELINE):
        raise SystemExit("published HTML inventory differs from the frozen 35-document inventory")
    changed = 0
    for relative in actual:
        path = HTML_ROOT / relative
        data = path.read_bytes()
        if START in data or END in data:
            stripped = strip_fragment(data)
            verify_baseline(relative, stripped)
            continue
        verify_baseline(relative, data)
        body = data.find(b"<body")
        if body < 0:
            raise SystemExit(f"{relative}: missing body element")
        close = data.find(b">", body)
        if close < 0:
            raise SystemExit(f"{relative}: malformed body element")
        path.write_bytes(data[: close + 1] + NAV_FRAGMENT + data[close + 1 :])
        changed += 1
    print(f"Applied canonical D60 navigation to {changed} document(s); {len(actual)} total")


def check() -> None:
    actual = sorted(p.relative_to(HTML_ROOT).as_posix() for p in HTML_ROOT.rglob("*.html"))
    if actual != sorted(BASELINE):
        raise SystemExit("published HTML inventory differs from the frozen 35-document inventory")
    for relative in actual:
        data = (HTML_ROOT / relative).read_bytes()
        for url in REQUIRED_URLS:
            if data.count(url) != 1:
                raise SystemExit(f"{relative}: required URL count is not one: {url.decode()}")
        if data.count(b'<nav class="program-matematika-global-nav"') != 1:
            raise SystemExit(f"{relative}: accessible navigation element missing or duplicated")
        stripped = strip_fragment(data)
        verify_baseline(relative, stripped)
    print("PASS: 35/35 D60 HTML readers contain one accessible bilingual nav; frozen bytes preserved")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("apply", "check"))
    args = parser.parse_args()
    if args.mode == "apply":
        apply()
    check()


if __name__ == "__main__":
    main()
