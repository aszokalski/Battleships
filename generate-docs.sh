#!/bin/sh
cd docs
sphinx-apidoc -fe -o source/ ../app/
make html
cd ..
ln -s docs/build/html/index.html docs.html