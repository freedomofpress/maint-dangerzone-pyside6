#!/usr/bin/env python

# NOTE: This script exists because finding outdated dependencies is a bit
# tricky with Poetry: https://github.com/python-poetry/poetry/issues/2684

import sys
import requests

PYPI_PACKAGES = [
    "PySide6",
    "PySide6_Addons",
    "PySide6_Essentials",
    "shiboken6",
]
WHEEL_TYPE = "cp38-abi3-manylinux_2_28_x86_64.whl"
EXPECTED_VERSION = "6.6.2"


def get_package_info(pkg):
    res = requests.get(f"https://pypi.org/pypi/{pkg}/json")
    res.raise_for_status()
    pkg_info = res.json()
    version = pkg_info["info"]["version"]
    sha256_digest = [
        w["digests"]["sha256"] for w in pkg_info["releases"][version]
        if w["filename"] == f"{pkg}-{version}-{WHEEL_TYPE}"
    ][0]
    return (version, sha256_digest)


def main():
    version_ok = True
    pkgs = {}
    for pkg in PYPI_PACKAGES:
        version, sha256_digest = get_package_info(pkg)
        pkgs[pkg] = {}
        pkgs[pkg]["version"] = version
        pkgs[pkg]["digest"] = sha256_digest
        if version != EXPECTED_VERSION:
            version_ok = False
            version_new = version

    for pkg, info in pkgs.items():
        print(f"{pkg} {info['version']} (digest: {info['digest']})")

    if not version_ok:
        print(f"Version mismatch detected", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
