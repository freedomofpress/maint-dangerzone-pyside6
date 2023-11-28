# FIXME: Some PySide6 files cannot be byte-compiled.
# https://devel.fedoraproject.narkive.com/vDcpjQEE/how-to-control-or-avoid-brp-python-bytecompile
%global _python_bytecompile_errors_terminate_build 0

# FIXME:: Disable compression to speed up builds:
# https://stackoverflow.com/questions/9292243/rpmbuild-change-compression-format
%define _source_payload w0.ufdio
%define _binary_payload w0.ufdio

# FIXME:: Fixes the "Missing build-id in ..." errors. Taken from:
# https://unix.stackexchange.com/questions/688839/if-i-do-not-care-about-debug-support-in-red-hat-packages-what-are-the-drawbacks
%define _build_id_links none

################################################################################
# Package Description

Name:           python3-pyside6
Version:        6.6.0
Release:        1%{?dist}
Summary:        Python bindings for Qt 6
License:        LGPL-3.0-only OR (GPL-2.0-only OR GPL-3.0-or-later) AND GPL-2.0-only AND GPL-3.0-only WITH Qt-GPL-exception-1.0
# FIXME: Get architecture automatically
Source0:         https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl
Source1:         https://download.qt.io/official_releases/QtForPython/pyside6/PySide6_Addons-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl
Source2:         https://download.qt.io/official_releases/QtForPython/pyside6/PySide6_Essentials-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl
Source3:         https://download.qt.io/official_releases/QtForPython/pyside6/shiboken6-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl

# FIXME: Automatic requirement discovery brings its own class of problems, so
# temporarily disable it.
AutoReqProv:    no

################################################################################
# Package Requirements
BuildRequires:   python3-devel

# Placates the Dangerzone requirement
Provides: python3.11dist(pyside6)

%description
PySide6 is the official Python module from the Qt for Python project, which
provides access to the complete Qt 6.0+ framework.

################################################################################
# Package Build Instructions

%prep
sha256sum -c <<EOF
d487eab0f9bfc5c9141b474093e16207ff48cd9335e6465a01deb8dff0693fbc  %SOURCE0
5c56e963b841aeaacbc9ca8ca34df45308818dbd6fc59faa2b5a00a299e9892b  %SOURCE1
60284641619f964e1cb4d53cf3169d7a385e0378b74edb75610918d2aea1c4e5  %SOURCE2
456b89fb4b323e0c5002d92e4d346b48bb4e709db801208df8a0d6b4f5efc33d  %SOURCE3
EOF

%install
%{__python3} -m pip install --no-cache-dir --no-index --root %{buildroot} \
    %SOURCE0 %SOURCE1 %SOURCE2 %SOURCE3
# manually.
# XXX: I don't see any reason to include these binary files, and they bring
# errors.
rm -r %{buildroot}/usr/bin
# XXX: Placate rpmbuild
chmod -x %{buildroot}%{python3_sitearch}/PySide6/scripts/pyside_tool.py

%files
%{python3_sitearch}/PySide6*
%{python3_sitearch}/shiboken6*

# TODO: Add a changelog
