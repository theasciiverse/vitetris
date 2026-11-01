#!/bin/sh
# Builds vitetris as one binary, out/vitetris. It needs no libraries:
# the terminal backend writes ANSI sequences itself, and the build
# options are upstream's committed config.mk and src/config.h (1- and
# 2-player, network play, terminal resizing, menus, block styles), so
# configure is not run.
#   Linux:  docker run --rm -v "$PWD":/src -w /src alpine:3.22 sh asciiverse/build.sh
#           (static, musl)
#   macOS:  CC_ARCH=arm64 sh asciiverse/build.sh   (or x86_64)
#   here:   sh asciiverse/build.sh                 (to try things)
set -eu
cd "$(dirname "$0")/.."
lflags=
if [ -f /etc/alpine-release ]; then
  apk add --no-cache build-base >/dev/null
  lflags=-static
fi
make clean >/dev/null 2>&1 || true
make CC="cc${CC_ARCH:+ -arch $CC_ARCH}" LDFLAGS="$lflags" PROGNAME=vitetris >/dev/null
rm -rf out && mkdir out
mv vitetris out/vitetris
