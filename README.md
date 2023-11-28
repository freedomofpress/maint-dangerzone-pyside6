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

## Build

You can build source and binary RPM packages with the following commands:

```sh
dnf install -y rpm-build python3-devel
./build.sh
```
