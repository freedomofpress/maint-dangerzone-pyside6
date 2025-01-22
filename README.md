**This repo is archived. Fedora now offers PySide6 packages across all of its
supported versions. See
https://github.com/freedomofpress/maint-dangerzone-pyside6/issues/5 for
details**

# Build instructions for PySide6 RPMs

Most popular distros [do not offer a PySide6 package](https://repology.org/project/python:pyside6/versions).
If you are a developer that needs Python Qt bindings, and you want to package
your application, you can't rely on virtualenvs. You do have some alternatives,
but they are not ideal:

1. Use PySide2 (`python3-pyside2`). There are several issues with this approach:
   * PySide2 does not support Python 3.12 yet (see [bug report](https://bugreports.qt.io/browse/PYSIDE-2230)).
     This has already bit Fedora 39, which has [retired](https://pagure.io/fesco/issue/3080)
     the `python3-pyside2` package from its repos.
   * PySide2 requires Qt5, [which is EOL](https://www.qt.io/blog/qt-5.15-extended-support-for-subscription-license-holders),
     placing the maintenance burden on distros.
2. Use [PyQt](https://riverbankcomputing.com/software/pyqt/intro) bindings.
   These bindings are GPL licensed, which are incompatible with non-GPL
   applications. Moreover, they are not official bindings, as they are provided
   by a third party.

This repo has information on how to package PySide6 alongside your application.
It was created to aid in the development of
[Dangerzone](https://github.com/freedomofpress/dangerzone), a multi-platform
GUI application that uses Qt. We recommend you take a look at the
[challenges](https://github.com/freedomofpress/dangerzone/issues/211#issuecomment-1827777122)
we encountered while packaging PySide6, in order to understand the design
choices in this repo.

> [!IMPORTANT]
> As of 2024-04-15, this repo will no longer build a PySide6 RPM greater than
> 6.6.3.1. The reason is that PySide6 6.7.0 [is now available](https://packages.fedoraproject.org/pkgs/python-pyside6/python3-pyside6/fedora-rawhide.html)
> in Fedora Rawhide, and will [soon be available](https://bugzilla.redhat.com/show_bug.cgi?id=2271325#c4)
> in the rest of the Fedora releases.
>
> **UPDATE:** On 2024-05-05, an update in Fedora's Python3 package triggered a
> a segfault in the PySide6 package (see [Bugzilla #2279088](https://bugzilla.redhat.com/show_bug.cgi?id=2279088)).
> Unfortunately, we can't wait for Fedora's PySide6 to reach the stable
> releases, so we have to package PySide6 6.7.1 ourselves.

## Build

You can build source and binary RPM packages with the following commands:

```sh
dnf install -y rpm-build python3-devel
./build.sh
```

You can also find nightly builds in our GitHub actions page.
