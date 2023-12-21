#!/bin/sh

set -e

BASEDIR=$(realpath $(dirname $0))

mkdir -p $BASEDIR/.rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
rpmbuild -v --define "_topdir $BASEDIR/.rpmbuild" \
    --undefine=_disable_source_fetch -ba $BASEDIR/python3-pyside6.spec

echo "Successfully created PySide6 RPMs. You can find them under:"
find  $BASEDIR/.rpmbuild/{S,}RPMS/ -type f
