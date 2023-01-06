#!/bin/sh
cd docs
make html
cd ..
ln -s docs/build/html/index.html docs.html