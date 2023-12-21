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

################################################################################
# Package Description

Name:           python3-pyside6
Version:        6.6.1
Release:        1%{?dist}
Summary:        Python bindings for Qt 6, including the Qt 6 library, backported from the official Python wheels
License:        LGPL-3.0-only OR (GPL-2.0-only OR GPL-3.0-or-later) AND GPL-2.0-only AND GPL-3.0-only WITH Qt-GPL-exception-1.0
Source0:        https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl
Source1:        https://download.qt.io/official_releases/QtForPython/pyside6/PySide6_Addons-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl
Source2:        https://download.qt.io/official_releases/QtForPython/pyside6/PySide6_Essentials-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl
Source3:        https://download.qt.io/official_releases/QtForPython/pyside6/shiboken6-%{version}-cp38-abi3-manylinux_2_28_x86_64.whl

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
0a67587c088cb80e90d4ce3023b02466ea858c93a6dc9c4e062b13314e03d464  %SOURCE0
a0982da4033319667f9df5ed6fa8eff300a88216aec103a1fff6751a172b19a0  %SOURCE1
c7185616083eab6f42eaed598d97d49fac4f60ae2e7415194140d54f58c2b42c  %SOURCE2
fb102e4bc210006f0cdd0ce38e1aaaaf792bd871f02a2b3f01d07922c5cf4c59  %SOURCE3
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
rm %{buildroot}%{python3_sitearch}/PySide6/{assistant,designer,linguist,lrelease,lupdate,qmlformat,qmllint,qmlls}
rm -r %{buildroot}%{python3_sitearch}/PySide6/Qt/{libexec,metatypes,qml,translations}/

# Remove any plugin that is NOT part of the core Qt 6 packages (qt6-qtbase*). We
# do this to keep the number of our dependencies in check. We originally
# retrieved this list with:
#
#    $ dnf repoquery --list qt6-qtbase* | grep -oP 'plugins/([[:alpha:]]+)' | sort  | uniq
#    Last metadata expiration check: 0:39:04 ago on Thu Dec 21 16:07:55 2023.
#    plugins/designer
#    plugins/egldeviceintegrations
#    plugins/generic
#    plugins/iconengines
#    plugins/imageformats
#    plugins/networkinformation
#    plugins/platforminputcontexts
#    plugins/platforms
#    plugins/platformthemes
#    plugins/printsupport
#    plugins/script
#    plugins/sqldrivers
#    plugins/styles
#    plugins/tls
#    plugins/xcbglintegrations
rm -r %{buildroot}%{python3_sitearch}/PySide6/Qt/plugins/{assetimporters,canbus,geometryloaders,geoservices,multimedia,position,qmltooling,renderers,renderplugins,sceneparsers,scxmldatamodel,sensors,texttospeech,wayland-*}
# SQL Mimer is a proprietary DB for which there are not packages in Fedora, and
# therefore this library cannot be loaded.
rm %{buildroot}%{python3_sitearch}/PySide6/Qt/plugins/sqldrivers/libqsqlmimer.so

rm -r %{buildroot}%{python3_sitearch}/shiboken6_generator/

# The entry_points.txt and RECORD files are tainted with references to the files
# we deleted above. Instead of editing them, we can outright remove them.  These
# files are missing from Fedora's python3-pyside2 RPM after all, so most
# probably they don't affect the installation.
rm %{buildroot}%{python3_sitearch}/PySide6-%{version}.dist-info/RECORD
rm %{buildroot}%{python3_sitearch}/PySide6_Addons-%{version}.dist-info/RECORD
rm %{buildroot}%{python3_sitearch}/PySide6_Essentials-%{version}.dist-info/RECORD
rm %{buildroot}%{python3_sitearch}/PySide6_Essentials-%{version}.dist-info/entry_points.txt

%files
%{python3_sitearch}/PySide6/
%{python3_sitearch}/PySide6-%{version}.dist-info/
%{python3_sitearch}/PySide6_Addons-%{version}.dist-info/
%{python3_sitearch}/PySide6_Essentials-%{version}.dist-info/
%{python3_sitearch}/shiboken6/
%{python3_sitearch}/shiboken6-%{version}.dist-info/

%changelog
* Thu Dec 21 2023 Alex Pyrgiotis <alex.p@freedom.press> - 6.6.1
  - Backported PySide6 using the latest Python wheel from the Qt website
