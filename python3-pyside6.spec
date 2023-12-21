# The PySide6 Python wheel ships with private Qt6 libraries included, which we
# need in order to avoid conflicts with the private API of system Qt 6
# libraries.  The auto requires and provides system [1] in RPM will detect these
# private libraries and will do two things:
#
# 1. It will add them in the Provides section of the package. This is bad
#    because other libraries cannot load them. Advertising them therefore means
#    that we will break other packages that depend on Qt 6 libraries.
# 2. It will add most of them in the Requires section of the package. This is
#    bad because in order to satisfy this dependency, RPM will install the
#    system Qt 6 libraries, which are not necessary. Second, some of those
#    libraries may not be available through the system Qt 6 libraries, e.g., due
#    to a newer version.
#
# The best way to approach this problem is to exclude any libQt6* library from
# the Provides / Requires sections [2]. Note that these libraries may still have
# dependencies to system libraries, so it's important to keep those, and just
# exclude the libQt6 inter-dependencies.
#
# [1]: https://docs.fedoraproject.org/en-US/packaging-guidelines/AutoProvidesAndRequiresFiltering/
# [2]: https://docs.fedoraproject.org/en-US/packaging-guidelines/AutoProvidesAndRequiresFiltering/#_private_libraries
%global _privatelibs libQt6.*\\.so.*
%global __provides_exclude_from ^(%{_privatelibs})$
%global __requires_exclude_from ^(%{_privatelibs})$
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

# FIXME:: Disable compression to speed up builds:
# https://stackoverflow.com/questions/9292243/rpmbuild-change-compression-format
%define _source_payload w0.ufdio
%define _binary_payload w0.ufdio

################################################################################
# Package Description

Name:           python3-pyside6
Version:        6.6.0
Release:        1%{?dist}
Summary:        Python bindings for Qt 6, including the Qt6 library, backported from the official Python wheels
License:        LGPL-3.0-only OR (GPL-2.0-only OR GPL-3.0-or-later) AND GPL-2.0-only AND GPL-3.0-only WITH Qt-GPL-exception-1.0
Source0:         https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl
Source1:         https://download.qt.io/official_releases/QtForPython/pyside6/PySide6_Addons-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl
Source2:         https://download.qt.io/official_releases/QtForPython/pyside6/PySide6_Essentials-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl
Source3:         https://download.qt.io/official_releases/QtForPython/pyside6/shiboken6-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl

################################################################################
# Package Requirements
BuildRequires:   python3-devel

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
# Invoke pip in a way that it doesn't leave traces outside the build directory.
%{python3} -m pip install \
    --no-cache-dir \
    --no-index \
    --no-warn-script-location \
    --root %{buildroot} \
    %SOURCE0 %SOURCE1 %SOURCE2 %SOURCE3

# OpenSUSE's package for PySide6 and Fedora's package for PySide2 don't include
# PySide6 programs (i.e., files under `/usr/bin`), or PySide scripts (i.e.,
# files under %{python3_sitearch}/PySide6/scripts). These types of files have
# been causing errors anyways, so it's simpler for us to remove them.
rm -r %{buildroot}/usr/bin/
rm -r %{buildroot}%{python3_sitearch}/PySide6/{glue,include,scripts,support,typesystems}/
rm %{buildroot}%{python3_sitearch}/PySide6/{assistant,designer,linguist,lrelease,lupdate,qmlformat,qmllint,qmlls,libpyside6qml.abi3.so.6.6}
rm -r %{buildroot}%{python3_sitearch}/PySide6/Qt/{libexec,metatypes,plugins,qml,resources,translations}/
rm %{buildroot}%{python3_sitearch}/PySide6/Qt/lib/libicu*

# The entry_points.txt and RECORD files are tainted with references to the files
# we deleted above. Instead of editing them, we can outright remove them.  These
# files are missing from Fedora's python3-pyside2 RPM after all, so most
# probably they don't affect the insstallation.
rm %{buildroot}%{python3_sitearch}/PySide6-%{version}.dist-info/RECORD
rm %{buildroot}%{python3_sitearch}/PySide6_Addons-%{version}.dist-info/RECORD
rm %{buildroot}%{python3_sitearch}/PySide6_Essentials-%{version}.dist-info/RECORD
rm %{buildroot}%{python3_sitearch}/PySide6_Essentials-%{version}.dist-info/entry_points.txt

# Next versions of PySide6 may introduce extra libraries or binaries, so we make
# an attempt here to explicitly include just the files we're interested in. If
# an installed file is not present in this list, the build will fail, and we can
# look into what new was introduced.
%files
%{python3_sitearch}/PySide6/*.{py,pyi,so,so.6.6,typed}
%{python3_sitearch}/PySide6/__pycache__/
%{python3_sitearch}/PySide6/Qt/lib/libQt*.{so,so.6,so.56}
%{python3_sitearch}/PySide6/QtAsyncio/__pycache__/
%{python3_sitearch}/PySide6/QtAsyncio/*.py
%{python3_sitearch}/PySide6-%{version}.dist-info/
%{python3_sitearch}/PySide6_Addons-%{version}.dist-info/
%{python3_sitearch}/PySide6_Essentials-%{version}.dist-info/
%{python3_sitearch}/shiboken6/*.{py,pyi,so,so.6.6,typed}
%{python3_sitearch}/shiboken6/__pycache__/
%{python3_sitearch}/shiboken6-%{version}.dist-info/

%changelog
* Thu Dec 21 2023 Alex Pyrgiotis <alex.p@freedom.press> - 6.6.0
  - Backported PySide6 using the latest Python wheel from the Qt website
