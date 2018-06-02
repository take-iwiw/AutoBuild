#!/bin/sh
set -eu

echo "[Build pj1]"
if [ $# -eq 1 ]; then
	cd $1
fi
pwd
cd projects/pj1/
if [ -e build ]; then
	rm -rf build
fi
mkdir build
cd build
cmake ..
make clean all


