# The PySide6 Python wheel ships with private Qt6 libraries included, which we
# need in order to avoid conflicts with the private API of system Qt 6
# libraries. The auto requires and provides system [1] in RPM will detect these
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
# The best way to approach this problem is to:
# 1. Exclude all dynamic libraries (.so files) from our Provides section [2].
#    After all, dependent packages should require only the Python dependencies.
# 2. Exclude any Qt-related library from our Requires section [2]. Note that
#    these libraries may still have dependencies to system libraries, so it's
#    important to keep those, and just exclude the Qt inter-dependencies.
#
# [1]: https://docs.fedoraproject.org/en-US/packaging-guidelines/AutoProvidesAndRequiresFiltering/
# [2]: https://docs.fedoraproject.org/en-US/packaging-guidelines/AutoProvidesAndRequiresFiltering/#_private_libraries
%global __provides_exclude ^(lib.*\\.so.*)
%global __requires_exclude ^(.*Qt6.*|.*pyside6.*|.*shiboken6.*|libicu.*\\.so.*)$

################################################################################
# Package Description

Name:           python3-pyside6
Version:        6.7.1
Release:        1%{?dist}
Summary:        Python bindings for Qt 6, including the Qt 6 library, backported from the official Python wheels
License:        LGPL-3.0-only OR (GPL-2.0-only OR GPL-3.0-or-later) AND GPL-2.0-only AND GPL-3.0-only WITH Qt-GPL-exception-1.0
Source0:        https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-%{version}-cp39-abi3-manylinux_2_28_x86_64.whl
Source1:        https://download.qt.io/official_releases/QtForPython/pyside6/PySide6_Addons-%{version}-cp39-abi3-manylinux_2_28_x86_64.whl
Source2:        https://download.qt.io/official_releases/QtForPython/pyside6/PySide6_Essentials-%{version}-cp39-abi3-manylinux_2_28_x86_64.whl
Source3:        https://download.qt.io/official_releases/QtForPython/pyside6/shiboken6-%{version}-cp39-abi3-manylinux_2_28_x86_64.whl

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
45a539286e3a8afafd3ebc6b3391d587ce86293564ecba3a994e335dc68fe599  %SOURCE0
e9fbfc31e0de5075ee98d92cdbd7ccd274e4ac25100c890ae5bddfc8804a304c  %SOURCE1
b2d70dc4376c1b1ff5b2988a428a0ed5a889173ce9a0b56803468063d0ef7c75  %SOURCE2
6322b7a6232fc93eac0b11489007734438ae1e6213429fd6d7521d04072c2f87  %SOURCE3
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
* Tue May 27 2024 Alex Pyrgiotis <alex.p@freedom.press> - 6.7.1
  - Packaged PySide6 6.7.1 using the Python wheel from the Qt website. This
    is an emergency release, to fix a segfault in Fedora 39+.

* Tue Apr 16 2024 Alex Pyrgiotis <alex.p@freedom.press> - 6.6.3.1
  - Packaged PySide6 6.6.3.1 using the Python wheel from the Qt website. This
    looks like the last FPF release, since PySide6 is already in Fedora Rawhide.

* Tue Feb 20 2024 Alex Pyrgiotis <alex.p@freedom.press> - 6.6.2
  - Packaged PySide6 using the latest Python wheel from the Qt website

* Thu Dec 21 2023 Alex Pyrgiotis <alex.p@freedom.press> - 6.6.1
  - Backported PySide6 using the latest Python wheel from the Qt website
