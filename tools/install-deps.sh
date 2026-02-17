#!/usr/bin/env bash

set -euo pipefail


curl -L https://github.com/symengine/symengine/archive/master.tar.gz | tar -xz
rm -f master.tar.gz
cmake -S"symengine-master" -B"symengine-master/build" -DBUILD_TESTS=OFF -DBUILD_BENCHMARKS=OFF -GNinja 
cmake --build "symengine-master/build" --target install 
rm -rf symengine-master 